import os
import logging
import socket
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
import csv
from flask import Flask, request, jsonify, render_template, flash, redirect, url_for, send_file
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
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

app = Flask(__name__, template_folder='templates')
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-here')
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

app.config['USE_REDIS'] = False

# Email config
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
SMTP_USE_TLS = os.getenv('SMTP_USE_TLS', 'true').lower() == 'true'
SMTP_USE_SSL = os.getenv('SMTP_USE_SSL', 'false').lower() == 'true'
SMTP_TIMEOUT = int(os.getenv('SMTP_TIMEOUT', 10))


# Initialize LoginManager
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))

# User loader function
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
     db.create_all()

class ProspectData(BaseModel):
    name: str
    company: str
    role: str
    website: Optional[str] = None
    email: Optional[str] = None

    @validator('email')
    def validate_email_format(cls, v):
        if v:
            regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            if not re.match(regex, v):
                raise ValueError('Invalid email format')
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
    """Send email via SMTP with comprehensive error handling"""
    # Validate configuration
    if not all([EMAIL_ADDRESS, EMAIL_PASSWORD, SMTP_SERVER]):
        app.logger.error("Email configuration incomplete")
        return False

    # Validate recipient email
    if not to_email or '@' not in to_email:
        app.logger.error(f"Invalid recipient email: {to_email}")
        return False

    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Establish server connection
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10) as server:
            server.ehlo()  # Identify ourselves to the SMTP server
            
            if SMTP_USE_TLS:
                server.starttls()  # Secure the connection
                server.ehlo()  # Re-identify ourselves over TLS connection
            
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        
        app.logger.info(f"Email successfully sent to {to_email}")
        return True

    except smtplib.SMTPAuthenticationError:
        app.logger.error("SMTP Authentication failed - check username/password")
    except smtplib.SMTPRecipientsRefused as e:
        app.logger.error(f"Recipient refused: {e.recipients}")
    except smtplib.SMTPSenderRefused:
        app.logger.error("Sender address refused - check FROM email")
    except smtplib.SMTPException as e:
        app.logger.error(f"SMTP error occurred: {str(e)}")
    except socket.timeout:
        app.logger.error("SMTP connection timed out")
    except Exception as e:
        app.logger.error(f"Unexpected error sending email: {str(e)}")
    
    return False

app.route('/send-email', methods=['POST'])
def send_email_endpoint():
    """
    Endpoint for sending emails
    Expects JSON payload with:
    {
        "to_email": "recipient@example.com",
        "subject": "Email Subject",
        "body": "Email content here"
    }
    """
    if not request.is_json:
        return jsonify({
            'success': False,
            'message': 'Request must be JSON'
        }), 400

    data = request.get_json()
    
    # Validate required fields
    required_fields = ['to_email', 'subject', 'body']
    if not all(field in data for field in required_fields):
        return jsonify({
            'success': False,
            'message': f'Missing required fields: {required_fields}'
        }), 400

    # Send the email
    result = send_email(
        to_email=data['to_email'],
        subject=data['subject'],
        body=data['body']
    )

    if result['success']:
        return jsonify(result), 200
    else:
        return jsonify(result), 500

@app.route('/test-email')
def test_email_endpoint():
    """
    Test endpoint to verify email sending works
    """
    test_email = EMAIL_ADDRESS or 'recipient@example.com'
    result = send_email(
        to_email=test_email,
        subject='Test Email from Flask App',
        body='This is a test email to verify your email sending functionality is working.'
    )
    
    return jsonify(result)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/documentation')
def documentation():
    return render_template('documentation.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/api')
def api():
    return render_template('api.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/careers')
def careers():
    return render_template('careers.html')

@app.route('/features')
def features():
    return render_template('features.html')

@app.route('/gdpr')
def gdpr():
    return render_template('gdpr.html')

@app.route('/guide')
def guide():
    return render_template('guide.html')

@app.route('/account')
def account():
    return render_template('account.html')

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/logs/<path:filename>')
@login_required
def view_log(filename):
    safe_path = os.path.join(app.config.get('LOG_FOLDER', 'logs'), secure_filename(filename))
    if os.path.exists(safe_path):
        return send_file(safe_path)
    return "Log file not found", 404

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        
        user = User.query.filter_by(email=email).first()
        
        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('login'))
        
        login_user(user, remember=remember)
        return redirect(url_for('dashboard'))
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        
        # Validate inputs
        if not email or not name or not password:
            flash('All fields are required!', 'error')
            return redirect(url_for('register'))
        
        try:
            # Check if user exists
            user = User.query.filter_by(email=email).first()
            if user:
                flash('Email address already exists', 'error')
                return redirect(url_for('register'))
            
            # Create new user with correct password hashing
            new_user = User(
                email=email,
                name=name,
                password=generate_password_hash(password, method='pbkdf2:sha256')  # Updated method
            )
            
            db.session.add(new_user)
            db.session.commit()
            
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Registration error: {str(e)}', 'error')
            return redirect(url_for('register'))
    
    return render_template('signup.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('index.html', name=current_user.name)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/generate', methods=['POST'])
@login_required
def handle_generation():
    try:
        # Validate request
        if not request.is_json and 'csv_file' not in request.files:
            return jsonify({'error': 'Invalid request format'}), 400

        if 'csv_file' in request.files:
            results = handle_csv()
            return jsonify({
                'success': True,
                'results': results
            })
        else:
            data = request.get_json()
            if not data:
                return jsonify({'error': 'No JSON data provided'}), 400
                
            result = handle_single(data)
            return jsonify({
                'success': True,
                'email': result['email'],
                'cost': result['cost']
            })
            
    except Exception as e:
        app.logger.error(f"Generation error: {str(e)}")
        return jsonify({'error': str(e)}), 500


def handle_single(data):
    prospect = ProspectData(**data)
    email_content = generate_email(prospect)
    
    if not email_content:
        raise ValueError('Failed to generate email')
    
    if prospect.email and data.get('send_email', False):
        subject = email_content.split('\n')[0].replace('Subject: ', '')
        body = '\n'.join(email_content.split('\n')[1:])
        if not send_email(prospect.email, subject, body):
            raise ValueError('Email generation succeeded but sending failed')
    
    return {
        'email': email_content,
        'cost': f"{lr.language_models.base.LLM.cost_summary().total:.4f}"
    }

def handle_csv():
    try:
        csv_file = request.files['csv_file']
        if not csv_file.filename.endswith('.csv'):
            raise ValueError('Only CSV files are allowed')
        
        filename = secure_filename(csv_file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        csv_file.save(filepath)
        
        results = []
        with open(filepath) as f:
            reader = csv.DictReader(f)
            for row in reader:
                result = {'prospect': row, 'status': '', 'email': None}
                try:
                    prospect = ProspectData(**row)
                    email_content = generate_email(prospect)
                    
                    if not email_content:
                        result['status'] = 'Failed to generate email'
                        results.append(result)
                        continue
                    
                    result['email'] = email_content
                    
                    if prospect.email and request.form.get('send_emails') == 'true':
                        subject = email_content.split('\n')[0].replace('Subject: ', '')
                        body = '\n'.join(email_content.split('\n')[1:])
                        send_success = send_email(prospect.email, subject, body)
                        result['status'] = 'Email sent' if send_success else 'Generated but failed to send'
                    else:
                        result['status'] = 'Generated (not sent)'
                    
                    results.append(result)
                
                except Exception as e:
                    result['status'] = f'Error: {str(e)}'
                    results.append(result)
        
        os.remove(filepath)
        return results
    
    except Exception as e:
        app.logger.error(f"CSV processing error: {str(e)}")
        raise  # Re-raise to be caught in the main handler

if __name__ == '__main__':
    app.run(debug=os.getenv('FLASK_DEBUG', 'false').lower() == 'true')

