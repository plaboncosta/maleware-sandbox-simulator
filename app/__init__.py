import os
from flask import Flask
from dotenv import load_dotenv


def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = 'samples'
    app.secret_key = os.getenv('SECRET_KEY')

    from .routes import main
    app.register_blueprint(main)
    return app
