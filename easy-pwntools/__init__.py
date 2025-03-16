from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    os.makedirs(app.config['UPLOAD_PATH'], exist_ok=True)

    from .views import main_views
    app.register_blueprint(main_views.bp)

    return app