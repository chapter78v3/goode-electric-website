"""Routes for Goode Electric website"""
import html
from flask import Blueprint, render_template, request, jsonify, current_app
from app.models import SERVICES, TESTIMONIALS, ContactForm
from app.security import limiter

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Home page"""
    featured_testimonials = TESTIMONIALS[:3]
    return render_template('index.html', testimonials=featured_testimonials)

@main_bp.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@main_bp.route('/services')
def services():
    """Services page"""
    return render_template('services.html', services=SERVICES)

@main_bp.route('/testimonials')
def testimonials():
    """Testimonials page"""
    return render_template('testimonials.html', testimonials=TESTIMONIALS)

def _field(data, key):
    """Pull one form field as a trimmed string.

    JSON gives callers full control of the value's type, so a dict or list
    here used to raise AttributeError on .strip() and return a 500. Anything
    that is not a string is rejected as empty and fails validation normally.
    """
    value = data.get(key, '')
    if not isinstance(value, str):
        return ''
    return value.strip()


@main_bp.route('/contact', methods=['GET', 'POST'])
@limiter.limit('5 per hour; 2 per minute', methods=['POST'])
def contact():
    """Contact page and form submission"""
    if request.method == 'POST':
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return jsonify({'success': False, 'error': 'Invalid request'}), 400

        form = ContactForm(
            name=_field(data, 'name'),
            email=_field(data, 'email'),
            phone=_field(data, 'phone'),
            subject=_field(data, 'subject'),
            message=_field(data, 'message')
        )

        error = form.validation_error()
        if error:
            return jsonify({'success': False, 'error': error}), 400

        # Send email
        success = send_email(form)

        if success:
            return jsonify({'success': True, 'message': 'Thank you! We\'ll contact you soon.'}), 200
        else:
            return jsonify({'success': False, 'error': 'Failed to send message. Please try again.'}), 500

    return render_template('contact.html')

def send_email(form):
    """Send the contact form to the shop via Azure Communication Services.

    Returns True only when ACS has accepted the message. When no connection
    string is configured we log the submission instead - a convenience for
    local development, so outside DEBUG it counts as a failure rather than
    silently dropping a customer enquiry.
    """
    conn = current_app.config.get('ACS_CONNECTION_STRING')
    if not conn:
        if current_app.config.get('DEBUG'):
            current_app.logger.info(
                'ACS not configured; contact form from %s (%d char message) not sent',
                form.email, len(form.message)
            )
            return True
        current_app.logger.error(
            'ACS_CONNECTION_STRING is not set - cannot send contact form'
        )
        return False

    # Imported lazily so the app still boots if the SDK is missing locally
    from azure.communication.email import EmailClient

    plain = (
        "New contact form submission:\n\n"
        f"Name: {form.name}\n"
        f"Email: {form.email}\n"
        f"Phone: {form.phone}\n"
        f"Subject: {form.subject}\n\n"
        f"Message:\n{form.message}\n"
    )

    # form fields are attacker-controlled, so escape before embedding in HTML
    rows = "".join(
        f"<tr><td><strong>{html.escape(label)}</strong></td>"
        f"<td>{html.escape(value or '')}</td></tr>"
        for label, value in (
            ('Name', form.name),
            ('Email', form.email),
            ('Phone', form.phone),
            ('Subject', form.subject),
        )
    )
    body_html = (
        "<h3>New contact form submission</h3>"
        f"<table cellpadding='4'>{rows}</table>"
        "<p><strong>Message</strong><br>"
        f"{html.escape(form.message).replace(chr(10), '<br>')}</p>"
    )

    message = {
        'senderAddress': current_app.config['ACS_SENDER_ADDRESS'],
        'recipients': {
            'to': [{'address': current_app.config['RECIPIENT_EMAIL']}],
        },
        # lets the shop hit reply and reach the customer directly
        'replyTo': [{'address': form.email, 'displayName': form.name}],
        'content': {
            'subject': f'Website Contact: {form.subject}',
            'plainText': plain,
            'html': body_html,
        },
    }

    try:
        client = EmailClient.from_connection_string(conn)
        poller = client.begin_send(message)
        result = poller.result(timeout=current_app.config.get('ACS_SEND_TIMEOUT', 30))
    except Exception:
        current_app.logger.exception('Failed to send contact form via ACS')
        return False

    status = (result or {}).get('status')
    if status != 'Succeeded':
        current_app.logger.error('ACS returned status %s for contact form', status)
        return False

    current_app.logger.info(
        'Contact form sent via ACS (id=%s)', (result or {}).get('id')
    )
    return True

@main_bp.route('/api/services')
def api_services():
    """API endpoint for services"""
    return jsonify(SERVICES)

@main_bp.route('/api/testimonials')
def api_testimonials():
    """API endpoint for testimonials"""
    return jsonify(TESTIMONIALS)
