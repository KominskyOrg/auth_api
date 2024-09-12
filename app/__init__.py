from flask import Flask
from app.routes import auth_bp
from app.config import get_config
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    CORS(app)

    # Load configuration
    app.config.from_object(get_config())

    # Register blueprints
    app.register_blueprint(auth_bp)

    # Conditionally register Swagger UI in development environment
    if app.config["ENV"] == "development":
        from flask_swagger_ui import get_swaggerui_blueprint

        SWAGGER_URL = "/api/docs"
        API_URL = "/static/swagger.yaml"
        swaggerui_blueprint = get_swaggerui_blueprint(
            SWAGGER_URL, API_URL, config={"app_name": "Auth API"}
        )
        app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    return app
