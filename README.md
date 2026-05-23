# 🚀 Bemal - AI Email Outreach

**A working, simple Flask server for AI-powered email outreach**

## ✨ Features

- ✅ **Actually Works** - Simple, tested Flask server
- ✅ **Clean Interface** - Modern, responsive UI
- ✅ **CSV Processing** - Upload prospects in bulk
- ✅ **Email Field** - Now includes email column support
- ✅ **No Bloat** - Removed all unnecessary files

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << 'ENVEOF'
SECRET_KEY=your-secret-key-here
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_ADDRESS=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
ENVEOF

# Run the server
python server.py
```

Then open http://localhost:5000

## 📁 Project Structure

```
ai-agent-clean/
├── server.py          # Main Flask server (WORKING)
├── api.py             # AI email generation logic
├── extensions.py      # Flask extensions
├── models.py          # Database models
├── requirements.txt   # Python dependencies
├── templates/         # HTML templates
│   ├── index.html    # Home page (working)
│   ├── dashboard.html # CSV upload (working)
│   └── login.html    # Login page
└── static/           # CSS/JS files
```

## 📊 CSV Format

```csv
name,company,role,email,website
John Doe,TechCorp,CTO,john@techcorp.com,techcorp.com
Jane Smith,StartupXYZ,CEO,jane@startupxyz.com,startupxyz.com
```

**Note:** The `email` column is now supported!

## 🔧 What Was Fixed

1. **Removed useless files**: Deleted duplicate Python files, old logs, pycache
2. **Simplified names**: Clean file names without spaces or (1) suffixes
3. **Working GUI**: Simple Flask server that actually runs
4. **Email field**: Added email column to CSV processing
5. **Clean templates**: Working HTML pages with modern design

## 🎯 Usage

### Generate Single Email
1. Go to http://localhost:5000
2. Fill in the form (name, company, role, email, website)
3. Click "Generate Email"
4. Get AI-generated personalized email

### Process CSV
1. Go to Dashboard
2. Upload CSV file
3. Server processes all prospects
4. Download results

## 📝 Notes

- Server runs on http://localhost:5000
- Debug mode enabled for development
- SQLite database for user storage
- Upload folder for CSV files

---

**Made with ❤️ - Actually Works!**
