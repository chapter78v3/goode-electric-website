import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    # Azure Communication Services - transactional email for the contact form
    ACS_CONNECTION_STRING = os.environ.get('ACS_CONNECTION_STRING')
    ACS_SENDER_ADDRESS = os.environ.get('ACS_SENDER_ADDRESS', 'noreply@mail.goode-electric.com')
    RECIPIENT_EMAIL = os.environ.get('RECIPIENT_EMAIL', 'shawn@goode-electric.com')
    # Seconds to wait for ACS to accept the message before giving up on the request
    ACS_SEND_TIMEOUT = int(os.environ.get('ACS_SEND_TIMEOUT') or 30)
    MAPS_API_KEY = os.environ.get('MAPS_API_KEY')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    ACS_CONNECTION_STRING = None

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
