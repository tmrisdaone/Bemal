# 🚀 Bemal - AI Email Outreach Agent

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0+-green?style=for-the-badge&logo=flask)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen?style=for-the-badge)

**AI-Powered Cold Email Personalization & Outreach Automation**

*Generate personalized, high-converting cold emails at scale using advanced AI agents*

[Features](#-features) • [Quick Start](#-quick-start) • [Documentation](#-documentation) • [API Reference](#-api-reference) • [FAQ](#-faq)

</div>

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [API Endpoints](#-api-endpoints)
- [Project Structure](#-project-structure)
- [Security](#-security)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

**Bemal** is an advanced AI-driven email outreach platform that leverages multiple AI agents to research prospects, personalize content, and automate cold email campaigns. Built with Flask and powered by Langroid multi-agent systems, it transforms generic cold outreach into highly personalized, effective communication.

### Key Capabilities

- 🔍 **Automated Research**: AI agents research companies and prospects using DuckDuckGo
- ✍️ **Smart Personalization**: Generates personalized emails based on research findings
- 📧 **Batch Processing**: Upload CSV files to process hundreds of prospects simultaneously
- 🎨 **Modern UI**: Clean, responsive web interface with real-time updates
- 🔐 **Secure**: Environment-based configuration with secure credential management
- 📊 **Cost Tracking**: Monitor AI token usage and costs in real-time

---

## ✨ Features

### 🤖 Multi-Agent AI System
- **Researcher Agent**: Gathers company and prospect information
- **Personalizer Agent**: Crafts personalized email content
- **Quality Checker**: Validates email quality and relevance

### 📬 Email Automation
- SMTP integration (Gmail, Outlook, custom servers)
- CSV import/export for batch processing
- Automatic threading and reply handling
- HTML and plain text support

### 🎯 Personalization Engine
- Company-specific hooks
- Role-based messaging
- Industry-aware content
- Dynamic value propositions

### 📊 Analytics & Tracking
- Real-time cost monitoring
- Token usage statistics
- Success rate tracking
- Export results to CSV/JSON

### 🛡️ Security Features
- Environment variable configuration
- Secure password hashing
- Session management
- CSRF protection

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Web Interface (Flask)                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Dashboard   │  │  CSV Upload  │  │  Results     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Application Layer                         │
│  ┌──────────────────┐  ┌──────────────────┐                 │
│  │  Route Handlers  │  │  Email Service   │                 │
│  └──────────────────┘  └──────────────────┘                 │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                     AI Agent Layer                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Researcher  │  │  Personalizer│  │  Validator   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   External Services                          │
│  DuckDuckGo API  │  SMTP Server  │  LLM Provider            │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Installation

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Git

### Quick Install

```bash
# Clone the repository
git clone https://github.com/jaydenmayers2436/Bemal.git
cd Bemal

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run setup wizard
python setup.py
```

### One-Command Setup

```bash
python setup.py
```

The setup wizard will:
- Create virtual environment
- Install all dependencies
- Generate `.env` configuration file
- Initialize the database
- Provide next steps

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the root directory:

```bash
# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_ADDRESS=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
SMTP_USE_TLS=true

# AI Configuration
GROQ_API_KEY=your-groq-api-key
MODEL=groq/llama3-70b-8192

# Security
SECRET_KEY=your-secret-key  # Auto-generated by setup.py

# Optional: Redis (for caching)
REDIS_HOST=localhost
REDIS_PORT=6379
```

### Getting Gmail App Password

1. Go to [Google Account Settings](https://myaccount.google.com/security)
2. Enable 2-Factor Authentication
3. Generate an [App Password](https://myaccount.google.com/apppasswords)
4. Use this password in `.env`

---

## 💡 Usage

### Web Interface

```bash
# Start the application
python app (1).py

# Access at http://localhost:5000
```

### Command Line (Batch Processing)

```bash
# Run individual agent
python agent1 (1).py

# Run Streamlit UI
streamlit run agent (1).py
```

### Email Sender Script

```bash
# Send batch emails
python email_sender.py
```

### CSV Format

Create a `prospects.csv`:

```csv
name,company,role,website,linkedin
"John Doe","TechCorp","CTO","techcorp.com","linkedin.com/in/johndoe"
"Jane Smith","StartupXYZ","CEO","startupxyz.com","linkedin.com/in/janesmith"
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Home page |
| `GET` | `/dashboard` | User dashboard |
| `POST` | `/generate` | Generate single email |
| `POST` | `/upload` | Process CSV file |
| `POST` | `/send-email` | Send email |
| `GET` | `/login` | User login |
| `POST` | `/register` | User registration |
| `GET` | `/results` | View generated emails |

### Example API Call

```bash
curl -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "company": "TechCorp",
    "role": "CTO",
    "website": "techcorp.com"
  }'
```

---

## 📁 Project Structure

```
Bemal/
├── app (1).py              # Main Flask application
├── ap (1).py               # API routes and handlers
├── Agent2 (1).py           # Secondary agent logic
├── agent (1).py            # Streamlit agent interface
├── agent1 (1).py           # Primary CLI agent
├── config.py               # Configuration management
├── extensions.py           # Flask extensions
├── models.py               # Database models
├── email_sender.py         # Standalone email sender
├── setup.py                # Setup wizard
├── run (1).py               # Application runner
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables
├── users.db                # SQLite database
│
├── templates/              # HTML templates
│   ├── index.html
│   ├── dashboard.html
│   ├── login.html
│   └── ...
│
├── static/                 # Static files
│   └── style.css
│
├── logs/                   # Application logs
└── instance/               # Instance-specific files
```

---

## 🔒 Security

### Best Practices

✅ **Do:**
- Use environment variables for secrets
- Enable 2FA on email accounts
- Use app-specific passwords
- Regularly rotate API keys
- Keep dependencies updated

❌ **Don't:**
- Commit `.env` files to Git
- Share API keys publicly
- Use production credentials in development
- Store passwords in plain text

### Security Features

- Password hashing with Werkzeug
- Session-based authentication
- CSRF protection
- Input validation
- SQL injection prevention (SQLAlchemy ORM)

---

## 🐛 Troubleshooting

### Common Issues

#### ModuleNotFoundError

```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

#### Authentication Failed

```bash
# Check .env configuration
# Ensure EMAIL_PASSWORD is an app password, not your regular password
# Verify 2FA is enabled
```

#### Port Already in Use

```bash
# Change port in run (1).py or use different port
python app (1).py --port 5001
```

#### AI Model Errors

```bash
# Verify GROQ_API_KEY is valid
# Check model name matches available models
# Ensure internet connection
```

### Getting Help

- Check [BUGFIX_SUMMARY.md](BUGFIX_SUMMARY.md) for known issues
- Review logs in `logs/` directory
- Open an issue on GitHub

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Clone and setup
git clone https://github.com/jaydenmayers2436/Bemal.git
cd Bemal
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run in debug mode
export FLASK_DEBUG=true
python app (1).py
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Langroid** - Multi-agent AI framework
- **Flask** - Web framework
- **Groq** - Fast LLM inference
- **DuckDuckGo** - Search API

---

## 📞 Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/jaydenmayers2436/Bemal/issues)
- **Email**: jaydenmayers66@gmail.com
- **Documentation**: See `/docs` folder

---

<div align="center">

**Made with ❤️ by [jaydenmayers2436](https://github.com/jaydenmayers2436)**

⭐ Star this repo if you find it helpful!

</div>
