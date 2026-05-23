# 🚀 Bemal - AI Email Outreach

<div align="center">

![Bemal](https://img.shields.io/badge/Bemal-AI%20Email%20Outreach-667eea?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0+-green?style=for-the-badge&logo=flask)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**AI-Powered Cold Email Personalization & Outreach Automation**

*Generate personalized, high-converting cold emails at scale*

[Features](#-features) • [Quick Start](#-quick-start) • [Setup Wizard](#-setup-wizard) • [Dashboard](#-dashboard) • [API](#-api-endpoints) • [FAQ](#-faq)

</div>

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Quick Start](#-quick-start)
- [Setup Wizard](#-setup-wizard)
- [Dashboard](#-dashboard)
- [Email History](#-email-history)
- [CSV Format](#-csv-format)
- [API Endpoints](#-api-endpoints)
- [Configuration](#-configuration)
- [Project Structure](#-project-structure)
- [FAQ](#-faq)
- [License](#-license)

---

## 🎯 Overview

**Bemal** is an advanced AI-driven email outreach platform that leverages multiple AI agents to research prospects, personalize content, and automate cold email campaigns. Built with Flask and powered by Langroid multi-agent systems, it transforms generic cold outreach into highly personalized, effective communication.

### Key Capabilities

- 🔍 **Automated Research**: AI agents research companies and prospects
- ✍️ **Smart Personalization**: Generates personalized emails based on findings
- 📧 **Batch Processing**: Upload CSV files to process hundreds of prospects
- 📊 **Analytics Dashboard**: Real-time stats on emails sent, success rates
- 📜 **Email History**: Track all sent emails with timestamps
- 🎨 **Modern UI**: Clean, responsive web interface
- 🔐 **No Login Required**: Open access, no authentication barriers

---

## ✨ Features

### 📊 Enhanced Dashboard
- **Real-time Statistics**: Emails sent today, this week, total processed
- **Success Rate Tracking**: Monitor your email campaign performance
- **Quick Email Generator**: Single prospect email generation
- **Batch CSV Processing**: Upload and process hundreds at once

### 📧 Email History
- **Complete Tracking**: View all sent emails with full content
- **Smart Filtering**: Filter by today, this week, this month, or all time
- **Timestamp Display**: See exactly when each email was sent
- **Status Badges**: Visual indicators for sent/failed emails

### 🤖 AI-Powered Generation
- **Multi-Agent System**: Researcher + Personalizer agents
- **Company Research**: Automatically gathers company info
- **Role-Based Messaging**: Tailored content for each prospect's role
- **Industry Awareness**: Context-aware email content

### 🎨 User Experience
- **Modern UI**: Beautiful gradient design with smooth animations
- **Responsive**: Works on desktop, tablet, and mobile
- **Drag & Drop**: Easy CSV file upload
- **Real-time Feedback**: Loading states and success messages

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Gmail account (or other SMTP provider)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/tmrisdaone/Bemal.git
cd Bemal

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the setup wizard
python setup.py

# 4. Start the server
python server.py

# 5. Open your browser
# http://localhost:5000
```

That's it! You're ready to send personalized emails. 🎉

---

## ⚙️ Setup Wizard

The interactive setup wizard makes configuration easy:

```bash
python setup.py
```

### What it does:
1. ✅ Asks for your email address
2. ✅ Guides you through Gmail App Password setup
3. ✅ Configures SMTP settings automatically
4. ✅ Tests your email connection
5. ✅ Saves configuration to `.env` file

### Gmail App Password Setup:

1. Go to [Google Account Settings](https://myaccount.google.com/security)
2. Enable **2-Factor Authentication** (if not already enabled)
3. Visit [App Passwords](https://myaccount.google.com/apppasswords)
4. Select "Mail" and your device
5. Copy the 16-character password
6. Use this password in the setup wizard

---

## 📊 Dashboard

The dashboard provides comprehensive analytics:

### Statistics Cards:
1. **Emails Sent Today**: Count from midnight
2. **Emails This Week**: Week-to-date count with success rate
3. **People Processed**: Total prospects with today's count
4. **Failed Emails**: Failed count vs successfully sent

### Quick Actions:
- **Generate Single Email**: Fill form for one prospect
- **Batch CSV Upload**: Process multiple prospects at once
- **View History**: Navigate to email history page

---

## 📧 Email History

Access at: `http://localhost:5000/history`

### Features:
- **Filter Options**:
  - All Time
  - Today
  - This Week
  - This Month

- **Each Email Shows**:
  - Recipient email address
  - Subject line
  - Full email body
  - Exact timestamp
  - Relative time (e.g., "2 hours ago")
  - Status badge (sent/failed)

---

## 📄 CSV Format

For batch processing, create a CSV file with these columns:

```csv
name,company,role,email,website
John Doe,TechCorp,CTO,john@techcorp.com,techcorp.com
Jane Smith,StartupXYZ,CEO,jane@startupxyz.com,startupxyz.com
Bob Johnson,Enterprise Inc,VP Sales,bob@enterprise.com,enterprise.com
```

### Required Columns:
- `name` - Full name of the prospect
- `company` - Company name

### Optional Columns:
- `role` - Job title
- `email` - Email address
- `website` - Company website

---

## 📡 API Endpoints

All endpoints return JSON responses.

### Generate Single Email

**POST** `/generate`

```json
{
  "name": "John Doe",
  "company": "TechCorp",
  "role": "CTO",
  "email": "john@techcorp.com",
  "website": "techcorp.com"
}
```

**Response:**
```json
{
  "success": true,
  "email": "Subject: Quick question...\n\nHi John,...",
  "prospect_id": 1
}
```

### Upload CSV

**POST** `/upload`

Upload a CSV file using multipart/form-data.

**Response:**
```json
{
  "success": true,
  "count": 10,
  "results": [
    {
      "name": "John Doe",
      "company": "TechCorp",
      "status": "success",
      "generated_email": "Subject:..."
    }
  ]
}
```

### Send Email

**POST** `/send`

```json
{
  "to": "john@example.com",
  "subject": "Quick question",
  "body": "Email body content..."
}
```

### Get Dashboard Stats

**GET** `/api/stats`

**Response:**
```json
{
  "emails_total": 150,
  "emails_today": 25,
  "emails_week": 87,
  "prospects_total": 200,
  "prospects_today": 30,
  "sent_count": 145,
  "failed_count": 5,
  "success_rate": 96.7
}
```

---

## ⚙️ Configuration

### Environment Variables (.env)

```env
# Security
SECRET_KEY=your-secret-key-here

# Email Configuration
EMAIL_ADDRESS=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USE_TLS=true
SMTP_USE_SSL=false
SMTP_TIMEOUT=10

# Database
DATABASE_URL=sqlite:///bemal.db
```

### SMTP Settings by Provider:

| Provider | SMTP Server | Port | TLS |
|----------|-------------|------|-----|
| Gmail | smtp.gmail.com | 587 | Yes |
| Outlook | smtp.office365.com | 587 | Yes |
| Yahoo | smtp.mail.yahoo.com | 587 | Yes |
| Custom | Your provider's server | As specified | As specified |

---

## 📁 Project Structure

```
Bemal/
├── server.py              # Main Flask application
├── api.py                 # Email generation logic
├── extensions.py          # Flask extensions setup
├── models.py              # Database models (EmailLog, Prospect)
├── setup.py               # Interactive setup wizard
├── requirements.txt       # Python dependencies
├── .env                   # Configuration (created by setup.py)
├── instance/
│   └── bemal.db          # SQLite database
├── uploads/              # CSV upload directory
└── templates/
    ├── dashboard.html     # Main dashboard with stats
    ├── history.html       # Email history page
    └── ...               # Other templates
```

---

## 🤖 FAQ

### Q: Do I need to create an account?
**A:** No! Bemal has no login barriers. Just run the server and start using it.

### Q: Is my data stored?
**A:** All data is stored locally in a SQLite database (`instance/bemal.db`). No data is sent to external servers except for email delivery via SMTP.

### Q: Can I use this with non-Gmail accounts?
**A:** Yes! Just configure your SMTP settings in the `.env` file or during setup.

### Q: How do I view sent emails?
**A:** Navigate to `/history` in your browser to see all sent emails with filtering options.

### Q: Can I process multiple prospects at once?
**A:** Yes! Use the CSV upload feature on the dashboard to process hundreds of prospects in batch.

### Q: What's the success rate calculation?
**A:** Success rate = (Sent Emails / Total Emails) × 100

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- **Langroid** - Multi-agent AI framework
- **Flask** - Web framework
- **SMTP** - Email delivery protocol

---

<div align="center">

**Made with ❤️ by [tmrisdaone](https://github.com/tmrisdaone)**

⭐ Star this repo if you find it helpful!

**Last Updated:** 🕐 2026 年 5 月 23 日 周六 03:20

</div>
