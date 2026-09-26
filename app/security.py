"""Security hardening: rate limiting, response headers, CSP nonces.

Kept separate from the application factory so the policy is easy to review
in one place.
"""
import secrets

from flask import g, render_template, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# In-memory storage is per worker process. That is acceptable here because the
# app runs as a single small instance; if it is ever scaled out or given more
# gunicorn workers, point RATELIMIT_STORAGE_URI at Redis so the limit is shared.
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=['200 per hour'],
    storage_uri='memory://',
    strategy='fixed-window',
)


def _csp(nonce):
    """Content-Security-Policy.

    Scripts are restricted to self, the Bootstrap CDN, and this request's
    nonce - so injected inline script will not execute. Styles still need
    'unsafe-inline' because the templates use inline style attributes.
    """
    return '; '.join([
        "default-src 'self'",
        f"script-src 'self' https://cdn.jsdelivr.net 'nonce-{nonce}'",
        "style-src 'self' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com 'unsafe-inline'",
        "font-src 'self' https://cdnjs.cloudflare.com data:",
        "img-src 'self' data:",
        "connect-src 'self'",
        "frame-ancestors 'none'",
        "base-uri 'self'",
        "form-action 'self'",
        "object-src 'none'",
    ])


def init_security(app):
    """Wire rate limiting, security headers and error handlers onto the app."""
    limiter.init_app(app)

    @app.before_request
    def _make_nonce():
        g.csp_nonce = secrets.token_urlsafe(16)

    @app.context_processor
    def _expose_nonce():
        return {'csp_nonce': getattr(g, 'csp_nonce', '')}

    @app.after_request
    def _security_headers(response):
        nonce = getattr(g, 'csp_nonce', '')
        response.headers['Content-Security-Policy'] = _csp(nonce)
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response.headers['Permissions-Policy'] = (
            'geolocation=(), microphone=(), camera=(), payment=(), usb=()'
        )
        response.headers['Cross-Origin-Opener-Policy'] = 'same-origin'
        # Only meaningful over TLS, and the site is HTTPS-only in Azure.
        if request.is_secure or not app.debug:
            response.headers['Strict-Transport-Security'] = (
                'max-age=31536000; includeSubDomains'
            )
        # Do not advertise the server stack.
        response.headers['Server'] = 'web'
        return response

    # Registered on the app, not the blueprint: a blueprint errorhandler does
    # not catch routing 404s, so the custom page never rendered before.
    @app.errorhandler(404)
    def _not_found(error):
        return render_template('404.html'), 404

    @app.errorhandler(429)
    def _rate_limited(error):
        return (
            {'success': False, 'error': 'Too many requests. Please try again later.'},
            429,
        )

    @app.errorhandler(413)
    def _too_large(error):
        return ({'success': False, 'error': 'Request too large.'}, 413)

    @app.errorhandler(500)
    def _server_error(error):
        return render_template('500.html'), 500

    return app
