import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BASE_URL = os.getenv('BASE_URL', 'http://jkom.com')
    AUTH_SERVICE_PORT=5001
    
class LocalConfig(Config):
    DEBUG = True
    BASE_URL = 'http://jkom.com'
    ENV = 'development'

class DevConfig(Config):
    DEBUG = False
    BASE_URL = 'http://jkom.com'
    ENV = 'development'

class ProdConfig(Config):
    DEBUG = False
    BASE_URL = 'http://jkom.com'
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