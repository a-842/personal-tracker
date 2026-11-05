from flask import Flask
from dotenv import load_dotenv
import os

def create_app(config_name=None):
    # Load environment variables from .env file
    load_dotenv()

    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-me')

    from app.routes import main_bp
    app.register_blueprint(main_bp)

    return app