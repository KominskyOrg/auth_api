import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    True 
    
class LocalConfig(Config):
    DEBUG = True
    BASE_URL = 'http://auth_service:5000'

class DevConfig(Config):
    DEBUG = False

class ProdConfig(Config):
    DEBUG = False

def get_config():
    env = os.getenv('FLASK_ENV', 'local')
    if env == 'local':
        return LocalConfig
    elif env == 'dev':
        return DevConfig
    elif env == 'prod':
        return ProdConfig
    else:
        raise ValueError(f"Unknown environment: {env}")