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


class LocalConfig(Config):
    DEBUG = True
    BASE_URL = "http://jkom.com"
    ENV = "development"


class DevConfig(Config):
    DEBUG = False
    BASE_URL = "http://jkom.com"
    ENV = "development"


class ProdConfig(Config):
    DEBUG = False
    BASE_URL = "http://jkom.com"
    ENV = "production"


def get_config():
    env = os.getenv("FLASK_ENV", "local")
    logger.debug(f"FLASK_ENV: {env}")  # Replaced print with logger.debug
    if env == "local":
        return LocalConfig
    elif env == "development":
        return DevConfig
    elif env == "production":
        return ProdConfig
    else:
        logger.error(f"Unknown environment: {env}")
        raise ValueError(f"Unknown environment: {env}")
