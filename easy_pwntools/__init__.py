from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    os.makedirs(app.config['UPLOAD_PATH'], exist_ok=True)

    from .routes import routes_list
    routes_list(app)

    return app