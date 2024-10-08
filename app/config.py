import os
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


class Config:
    BASE_URL = os.getenv("BASE_URL", "http://localhost")
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
