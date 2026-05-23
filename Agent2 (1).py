import os
import csv
from flask import Flask, request, jsonify, render_template, flash, redirect
from pydantic import BaseModel, validator
from typing import Optional, List
import langroid as lr
from langroid.agent.chat_agent import ChatAgent, ChatAgentConfig
from langroid.agent.task import Task
from langroid.language_models import OpenAIGPTConfig
from langroid.agent.tools.duckduckgo_search_tool import DuckduckgoSearchTool
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder='templates')
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Email config (set these in .env)
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

class ProspectData(BaseModel):
    name: str
    company: str
    role: str
    website: Optional[str] = None
    email: Optional[str] = None

    @validator('email', pre=True)
    def validate_email(cls, v):
        if v and '@' not in v:
            raise ValueError('Invalid email address')
        return v

def generate_email(prospect: ProspectData) -> str:
    """Generate personalized email"""
    llm_config = OpenAIGPTConfig(
        chat_model="groq/llama3-70b-8192",
        temperature=0.3,
        max_output_tokens=500,
    )

    researcher = ChatAgent(ChatAgentConfig(
        name="Researcher",
        system_message="Find company info and prospect's public content",
        llm=llm_config,
    ))
    researcher.enable_message(DuckduckgoSearchTool)

    personalizer = ChatAgent(ChatAgentConfig(
        name="Personalizer",
        system_message=f"""
        Create a 3-4 line email with:
        1. Personal hook about {prospect.company}
        2. Value proposition
        3. Clear CTA
        """,
        llm=llm_config,
    ))

    research_task = Task(researcher, single_round=True)
    personalize_task = Task(personalizer, llm_delegate=True)
    personalize_task.add_sub_task(research_task)

    query = f"""
    Find info about:
    1. {prospect.company} {f'website:{prospect.website}' if prospect.website else ''}
    2. {prospect.name} {prospect.role} site:linkedin.com/in
    """
    
    result = personalize_task.run(query)
    return result.content if result else None

def send_email(to_email: str, subject: str, body: str) -> bool:
    """Send email via SMTP"""
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = to_email
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'plain'))
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Email sending failed: {e}")
        return False

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def handle_generation():
    if 'csv_file' in request.files:
        return handle_csv()
    return handle_single()

def handle_single():
    data = request.json
    try:
        prospect = ProspectData(**data)
        email_content = generate_email(prospect)
        
        if not email_content:
            return jsonify({'error': 'Failed to generate email'})
        
        if prospect.email and data.get('send_email', False):
            subject = email_content.split('\n')[0].replace('Subject: ', '')
            body = '\n'.join(email_content.split('\n')[1:])
            if not send_email(prospect.email, subject, body):
                return jsonify({'error': 'Email generation succeeded but sending failed'})
        
        return jsonify({
            'success': True,
            'email': email_content,
            'email_html': email_content.replace('\n', '<br>'),
            'cost': f"{lr.language_models.base.LLM.cost_summary().total:.4f}"
        })
    except Exception as e:
        return jsonify({'error': str(e)})

def handle_csv():
    try:
        csv_file = request.files['csv_file']
        if not csv_file.filename.endswith('.csv'):
            return jsonify({'error': 'Only CSV files are allowed'})
        
        filename = secure_filename(csv_file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        csv_file.save(filepath)
        
        results = []
        with open(filepath) as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    prospect = ProspectData(**row)
                    email_content = generate_email(prospect)
                    
                    if not email_content:
                        results.append({
                            'prospect': prospect.dict(),
                            'status': 'Failed to generate email',
                            'email': None
                        })
                        continue
                    
                    if prospect.email and request.form.get('send_emails') == 'true':
                        subject = email_content.split('\n')[0].replace('Subject: ', '')
                        body = '\n'.join(email_content.split('\n')[1:])
                        send_success = send_email(prospect.email, subject, body)
                        status = 'Email sent' if send_success else 'Generated but failed to send'
                    else:
                        status = 'Generated (not sent)'
                    
                    results.append({
                        'prospect': prospect.dict(),
                        'status': status,
                        'email': email_content
                    })
                
                except Exception as e:
                    results.append({
                        'prospect': row,
                        'status': f'Error: {str(e)}',
                        'email': None
                    })
        
        os.remove(filepath)
        return jsonify({'success': True, 'results': results})
    
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=os.getenv('FLASK_DEBUG', 'false').lower() == 'true')
