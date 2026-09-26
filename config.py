import os
from dotenv import load_dotenv

load_dotenv()

DEV_SECRET_KEY = 'dev-secret-key-change-in-production'


class Config:
    """Base configuration"""

    @classmethod
    def validate(cls):
        """Checked by create_app at startup. Override to enforce more."""
        return None

    SECRET_KEY = os.environ.get('SECRET_KEY') or DEV_SECRET_KEY
    # Azure Communication Services - transactional email for the contact form
    ACS_CONNECTION_STRING = os.environ.get('ACS_CONNECTION_STRING')
    ACS_SENDER_ADDRESS = os.environ.get('ACS_SENDER_ADDRESS', 'noreply@mail.goode-electric.com')
    RECIPIENT_EMAIL = os.environ.get('RECIPIENT_EMAIL', 'shawn@goode-electric.com')
    # Seconds to wait for ACS to accept the message before giving up on the request
    ACS_SEND_TIMEOUT = int(os.environ.get('ACS_SEND_TIMEOUT') or 30)
    MAPS_API_KEY = os.environ.get('MAPS_API_KEY')

    # Reject oversized bodies at the WSGI layer, before any parsing. The
    # contact form's own field caps are well inside this.
    MAX_CONTENT_LENGTH = 64 * 1024

    # Session cookie hardening. Nothing sets a session today, but these are
    # the defaults we want if anything ever does.
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE = True


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    SESSION_COOKIE_SECURE = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

    @classmethod
    def validate(cls):
        # Fail at startup rather than quietly running on a key that is
        # published in this repository.
        if cls.SECRET_KEY == DEV_SECRET_KEY:
            raise RuntimeError(
                'SECRET_KEY must be set in the environment for production'
            )


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    ACS_CONNECTION_STRING = None
    SESSION_COOKIE_SECURE = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
