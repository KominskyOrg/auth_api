import os
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class Config:
    BASE_URL = os.getenv("BASE_URL", "http://jkom.com")
    AUTH_SERVICE_PORT = 5001


class DevConfig(Config):
    DEBUG = True
    ENV = "development"


class StagingConfig(Config):
    DEBUG = False
    ENV = "staging"


class ProdConfig(Config):
    DEBUG = False
    ENV = "production"


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
