"""
Flask application factory for Sales By Twilight API.
"""

from flask import Flask
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


def create_app():
    """
    Create and configure the Flask application.
    
    Returns:
        Flask: The configured Flask application instance
    """
    app = Flask(__name__)
    
    # Load configuration from environment variables
    app.config['SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'dev-secret-key')
    app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'False') == 'true'
    
    # Database configuration
    app.config['DB_HOST'] = os.getenv('DB_HOST', 'localhost')
    app.config['DB_PORT'] = int(os.getenv('DB_PORT', 3306))
    app.config['DB_NAME'] = os.getenv('DB_NAME', 'sales_by_twilight')
    app.config['DB_USER'] = os.getenv('DB_USER', 'root')
    app.config['DB_PASSWORD'] = os.getenv('DB_PASSWORD', '')
    
    # Register blueprints (routes)
    from app.routes.category_routes import category_bp
    app.register_blueprint(category_bp)
    
    return app