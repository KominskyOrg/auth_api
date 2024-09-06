from flask import Flask
from .config import get_config

def create_app():
    app = Flask(__name__)
    config = get_config()
    app.config.from_object(config)

    from .routes import auth_bp
    app.register_blueprint(auth_bp)

    return app
