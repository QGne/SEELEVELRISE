from flask import Flask
# Register blueprints (e.g., for routes) here if needed
from .routes import main
#what happen if not import from main?
import secrets
import os
from dotenv import load_dotenv


def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = 'app/static/uploads'
    app.config['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

    # Register blueprints (e.g., for routes) here if needed
    # Set a secret key for the session
    secret_key = secrets.token_hex(16)
    app.secret_key = secret_key  # Replace 'your_secret_key' with a strong, random key
    #from .routes import main
    app.register_blueprint(main)

    return app
