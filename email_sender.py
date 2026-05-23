#!/usr/bin/env python3
"""
AI Email Outreach - Email Sender Script
Standalone script to send emails to multiple recipients
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class"""
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
    EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS', '')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
    SMTP_USE_TLS = os.getenv('SMTP_USE_TLS', 'true').lower() == 'true'
    SMTP_USE_SSL = os.getenv('SMTP_USE_SSL', 'false').lower() == 'true'
    SMTP_TIMEOUT = int(os.getenv('SMTP_TIMEOUT', 10))

def send_email(to_email: str, subject: str, body: str) -> bool:
    """Send a single email"""
    if not all([EMAIL_ADDRESS, EMAIL_PASSWORD]):
        print("❌ Email configuration incomplete")
        return False
        
    if not to_email or '@' not in to_email:
        print(f"❌ Invalid recipient email: {to_email}")
        return False
        
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=SMTP_TIMEOUT) as server:
            server.ehlo()
            if SMTP_USE_TLS:
                server.starttls()
                server.ehlo()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
            
        print(f"✅ Email sent to {to_email}")
        return True
        
    except Exception as e:
        print(f"❌ Email sending failed: {str(e)}")
        return False

def send_multiple_emails(email_list, subject: str, body: str) -> bool:
    """Send email to multiple recipients"""
    if not email_list:
        print("❌ No email addresses provided")
        return False
        
    success_count = 0
    total_count = len(email_list)
    
    for i, email in enumerate(email_list, 1):
        print(f"📧 Sending email {i}/{total_count} to {email}...")
        if send_email(email, subject, body):
            success_count += 1
            
    print(f"📬 Sent {success_count}/{total_count} emails")
    return success_count == total_count

def main():
    """Main execution"""
    print("📧 AI Email Outreach - Email Sender")
    print("=" * 50)
    
    # Example usage
    test_emails = [
        "test1@example.com",
        "test2@example.com", 
        "test3@example.com"
    ]
    
    subject = "Test Email from AI Outreach"
    body = "This is a test email sent via the AI Email Outreach script.\n\nBest regards,\nAI Outreach Team"
    
    print("🚀 Starting batch email send...")
    success = send_multiple_emails(test_emails, subject, body)
    
    if success:
        print("🎉 All emails sent successfully!")
    else:
        print("❌ Some emails failed to send")

if __name__ == "__main__":
    main()