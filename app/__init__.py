from flask import Flask
from app.routes import auth_bp
from app.config import get_config
from flask_cors import CORS
import logging

# Get the logger
logger = logging.getLogger(__name__)

def create_app():
    logger.info("Creating Flask application")
    app = Flask(__name__)
    CORS(app)

    # Load configuration
    config = get_config()
    app.config.from_object(config)
    logger.info(f"Loaded configuration: {config.__name__}")

    # Register blueprints
    app.register_blueprint(auth_bp)
    logger.info("Registered auth blueprint")

    # Conditionally register Swagger UI in development environment
    if app.config["ENV"] == "development":
        from flask_swagger_ui import get_swaggerui_blueprint

        SWAGGER_URL = "/api/docs"
        API_URL = "/static/swagger.yaml"
        swaggerui_blueprint = get_swaggerui_blueprint(
            SWAGGER_URL, API_URL, config={"app_name": "Auth API"}
        )
        app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
        logger.info("Registered Swagger UI blueprint")

    logger.info("Flask application created successfully")
    return app

# Add this line to expose the Flask app to uWSGI
app = create_app()
