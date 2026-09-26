import logging

from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

from config import config

def create_app(config_name='development'):
    """Application factory"""
    app = Flask(__name__)
    settings = config[config_name]
    settings.validate()
    app.config.from_object(settings)

    # Flask's logger defaults to WARNING outside debug, which silently dropped
    # every INFO line - including the ACS message id for each email sent.
    app.logger.setLevel(logging.DEBUG if app.debug else logging.INFO)

    # App Service terminates TLS and proxies to us, so the peer address is the
    # front end. Trust one hop of X-Forwarded-* so request.remote_addr is the
    # real client - without this every visitor shares one rate-limit bucket.
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

    from app.security import init_security
    init_security(app)

    # Register blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    return app
