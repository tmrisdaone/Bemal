import os
import secrets
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for the AI Email Outreach app"""
    
    # Core configuration
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
    EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS', '')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
    SMTP_USE_TLS = os.getenv('SMTP_USE_TLS', 'true').lower() == 'true'
    SMTP_USE_SSL = os.getenv('SMTP_USE_SSL', 'false').lower() == 'true'
    SMTP_TIMEOUT = int(os.getenv('SMTP_TIMEOUT', 10))
    
    # Security - generate secure random key if not set
    SECRET_KEY = os.getenv('SECRET_KEY') or secrets.token_hex(32)
    
    # Database configuration
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///users.db')
    
    # AI Configuration (optional)
    GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')
    
    @classmethod
    def validate(cls):
        """Validate required configuration values"""
        required_fields = ['SMTP_SERVER', 'SMTP_PORT', 'EMAIL_ADDRESS', 
                          'EMAIL_PASSWORD', 'SECRET_KEY']
        
        missing = [field for field in required_fields if not getattr(cls, field)]
        if missing:
            raise ValueError(f"Missing required configuration fields: {missing}")
            
        # Validate email format
        if '@' not in EMAIL_ADDRESS:
            raise ValueError("Invalid email address format")
            
        # Validate port
        if not (1 <= SMTP_PORT <= 65535):
            raise ValueError("SMTP port must be between 1 and 65535")
            
        return True

# Initialize configuration
Config.validate()