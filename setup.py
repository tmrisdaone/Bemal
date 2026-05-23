#!/usr/bin/env python3
"""
AI Email Outreach Setup Wizard
A complete setup wizard for the AI Email Outreach app
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def create_virtual_environment():
    """Create a Python virtual environment"""
    venv_path = Path("venv")
    if not venv_path.exists():
        print("🚀 Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True)
        print("✅ Virtual environment created at ./venv")
    else:
        print("ℹ️ Virtual environment already exists")

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    requirements_file = "requirements.txt"
    
    # Check if requirements.txt exists
    if not os.path.exists(requirements_file):
        print(f"❌ {requirements_file} not found. Creating it...")
        with open(requirements_file, "w") as f:
            f.write("""flask\nflask-login\nflask-sqlalchemy\nlangroid\npydantic\npython-dotenv\nwerkzeug\nemail-validator\n""")
    
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", requirements_file], check=True)
    print("✅ Dependencies installed")

def create_env_file():
    """Create .env file with configuration template"""
    env_path = Path(".env")
    if not env_path.exists():
        print("🔐 Creating .env file...")
        with open(env_path, "w") as f:
            f.write("""# AI Email Outreach Configuration\n\n# SMTP Server Settings\nSMTP_SERVER=smtp.gmail.com\nSMTP_PORT=587\nSMTP_USE_TLS=true\n\n# Email Credentials (use app password for Gmail)\nEMAIL_ADDRESS=your_email@gmail.com\nEMAIL_PASSWORD=your_app_password\n\n# Secret Key for Flask sessions\nSECRET_KEY=your-secret-key-here\n\n# Optional: GROQ API Key for AI features\n# GROQ_API_KEY=your-groq-api-key\n\n# Database path (default is users.db in project directory)\nDATABASE_URL=sqlite:///users.db\n""")
        print("✅ .env file created")
    else:
        print("ℹ️ .env file already exists")

def create_database():
    """Create database file if it doesn't exist"""
    print("🗄️ Creating database...")
    if not Path("users.db").exists():
        # Create empty database file
        with open("users.db", "w") as f:
            pass
        print("✅ Database created at users.db")
    else:
        print("ℹ️ Database already exists")

def create_readme():
    """Create README.md with setup instructions"""
    readme_path = Path("README.md")
    if not readme_path.exists():
        print("📝 Creating README.md...")
        content = """# 🚀 Neon AI Outreach - AI-Powered Cold Email Generator

## 🌌 Cyberpunk Theme Header

```
  ██████╗ ███████╗ ██████╗ ███████╗ ██╗   ██╗
  ██╔══██╗██╔════╝ ██╔═══██╗██╔════╝██╗   ██║
  ██████╔╝█████╗  ██║   ██║███████╗██║   ██║
  ██╔══██╗██╔══╝  ██║   ██║██╔════╝██║   ██║
  ██████╔╝███████╗╚██████╔╝███████╗╚██████╔╝
  ╚═════╝ ╚══════╝ ╚═════╝ ╚══════╝ ╚═════╝
   AI Outreach Automation for Sales Teams
```

## ✨ Features

- Generate hyper-personalized cold emails using AI
- Send emails directly from the platform
- Batch process hundreds of prospects from CSV
- Track email performance and engagement
- Secure, private, and self-hosted

## 🛠️ Setup Instructions

### 1. Clone or Download the Project

```bash
git clone https://github.com/yourusername/ai-outreach.git
cd ai-outreach
```

### 2. Run the Setup Wizard

```bash
python setup.py
```

### 3. Configure Your Environment

1. Fill in your SMTP credentials in `.env`:
   - `EMAIL_ADDRESS`: Your Gmail address
   - `EMAIL_PASSWORD`: Your Gmail app password (not regular password!)
   - `SECRET_KEY`: A random secret for Flask sessions

2. Run the setup script:
   ```bash
   python setup.py
   ```

### 4. Start the Application

```bash
python app.py
```

### 5. Access the Application

Open your browser and go to: `http://localhost:5000`

## 📁 Project Structure

- `app.py` - Main Flask application
- `templates/` - HTML templates
- `static/` - CSS and static files
- `venv/` - Virtual environment (created by setup)
- `users.db` - SQLite database for users

## 🧪 Testing

```bash
# Test email sending
python -c "from app import send_email; print(send_email('test@example.com', 'Test Subject', 'Test body'))"
```

## 🛠️ Configuration

| Variable | Description | Required |
|----------|-------------|----------|
| SMTP_SERVER | SMTP server address | Yes |
| SMTP_PORT | SMTP server port | Yes |
| EMAIL_ADDRESS | Your email address | Yes |
| EMAIL_PASSWORD | Your email password or app password | Yes |
| SECRET_KEY | Flask session secret key | Yes |
| GROQ_API_KEY | (Optional) API key for AI features | No |

## 🔒 Security Notes

- Never commit your `.env` file to version control
- Use Gmail app passwords for email authentication
- Keep your secret key secure - it protects user sessions

## 🐛 Troubleshooting

- **SMTP Connection Issues**: Check firewall settings, ensure port is open
- **Authentication Failed**: Verify email and password, check Gmail app password settings
- **Database Issues**: Delete users.db and restart to recreate
- **Dependency Issues**: Ensure you're using Python 3.8+ and pip is updated

## 📞 Support

For support or feature requests, contact: support@neonoutreach.dev

© 2023 Neon Outreach - All rights reserved.
"""
        with open(readme_path, "w") as f:
            f.write(content)
        print("✅ README.md created")

def main():
    """Main setup wizard"""
    print("=" * 60)
    print("  🌌 NEON AI OUTREACH SETUP WIZARD")
    print("=" * 60)
    
    # Create virtual environment
    create_virtual_environment()
    
    # Install dependencies
    install_dependencies()
    
    # Create environment file
    create_env_file()
    
    # Create database
    create_database()
    
    # Create documentation
    create_readme()
    
    print("\n" + "=" * 60)
    print("  🎉 SETUP COMPLETE!")
    print("=" * 60)
    print("📁 All files created successfully!")
    print("📁 Run 'python app.py' to start the application")
    print("📁 Don't forget to configure your .env file!")
    print("=" * 60)

if __name__ == "__main__":
    main()