import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    BASE_URL = os.getenv('BASE_URL', 'http://localhost:5000')
    
class LocalConfig(Config):
    DEBUG = True
    BASE_URL = 'http://localhost:5000'
    ENV = 'development'

class DevConfig(Config):
    DEBUG = False
    BASE_URL = 'http://localhost:5000'
    ENV = 'development'

class ProdConfig(Config):
    DEBUG = False
    ENV = 'production'

def get_config():
    env = os.getenv('FLASK_ENV', 'local')
    print(f"FLASK_ENV: {env}")  # Debugging line
    if env == 'local':
        return LocalConfig
    elif env == 'development':
        return DevConfig
    elif env == 'production':
        return ProdConfig
    else:
        raise ValueError(f"Unknown environment: {env}")