from flask import Flask
from dotenv import load_dotenv
import os

def create_app():
    """Create and configure the Flask application."""
    # Load environment variables from .env file
    load_dotenv()

    app = Flask(__name__)

    # Get configuration from environment variables
    app.config['DEBUG'] = os.getenv('DEBUG', 'False') == 'True'
    app.secret_key = os.getenv('SECRET_KEY')

    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app