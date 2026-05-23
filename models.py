"""Database models for Bemal AI Email Outreach."""
from extensions import db
from datetime import datetime


class EmailLog(db.Model):
    """Model to track all sent emails."""
    id = db.Column(db.Integer, primary_key=True)
    recipient = db.Column(db.String(255), nullable=False)
    subject = db.Column(db.String(500), nullable=False)
    body = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='sent')  # 'sent' or 'failed'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'recipient': self.recipient,
            'subject': self.subject,
            'body': self.body,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Prospect(db.Model):
    """Model to track processed prospects."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100))
    email = db.Column(db.String(255))
    website = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'company': self.company,
            'role': self.role,
            'email': self.email,
            'website': self.website,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
