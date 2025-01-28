import os
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)

class Config:
    BASE_URL = os.getenv("BASE_URL", "http://auth_service")
    AUTH_SERVICE_URL = os.getenv(
        "AUTH_SERVICE_URL", "http://auth_service:5001/service/auth"
    )
    AUTH_SERVICE_PORT = 5001
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

class DevConfig(Config):
    DEBUG = True
    ENV = "development"
    LOG_LEVEL = "DEBUG"
    logger.debug(f"DevConfig: {Config.AUTH_SERVICE_URL}")

class StagingConfig(Config):
    DEBUG = False
    ENV = "staging"
    LOG_LEVEL = "INFO"

class ProdConfig(Config):
    DEBUG = False
    ENV = "production"
    LOG_LEVEL = "WARNING"

def get_config():
    env = os.getenv("FLASK_ENV", "development")
    logger.debug(f"FLASK_ENV: {env}")
    if env == "development":
        return DevConfig
    elif env == "staging":
        return StagingConfig
    elif env == "production":
        return ProdConfig
    else:
        logger.error(f"Unknown environment: {env}")
        raise ValueError(f"Unknown environment: {env}")

# Determine the current configuration
config = get_config()
