"""Flask extensions initialization module."""
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize Flask-SQLAlchemy
db = SQLAlchemy()

# Initialize Flask-Login
login_manager = LoginManager()
