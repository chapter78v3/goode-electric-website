"""Routes for Goode Electric website"""
from flask import Blueprint, render_template, request, jsonify, current_app
from app.models import SERVICES, TESTIMONIALS, ContactForm
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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

@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page and form submission"""
    if request.method == 'POST':
        data = request.get_json()
        
        form = ContactForm(
            name=data.get('name', '').strip(),
            email=data.get('email', '').strip(),
            phone=data.get('phone', '').strip(),
            subject=data.get('subject', '').strip(),
            message=data.get('message', '').strip()
        )
        
        if not form.is_valid():
            return jsonify({'success': False, 'error': 'Please fill in all fields correctly'}), 400
        
        # Send email
        success = send_email(form)
        
        if success:
            return jsonify({'success': True, 'message': 'Thank you! We\'ll contact you soon.'}), 200
        else:
            return jsonify({'success': False, 'error': 'Failed to send message. Please try again.'}), 500
    
    return render_template('contact.html')

def send_email(form):
    """Send email via SMTP"""
    try:
        # For development, just print the message
        # In production, configure MAIL_SERVER, MAIL_USERNAME, etc. in .env
        if current_app.config.get('MAIL_SERVER'):
            msg = MIMEMultipart()
            msg['From'] = current_app.config['MAIL_DEFAULT_SENDER']
            msg['To'] = current_app.config['RECIPIENT_EMAIL']
            msg['Subject'] = f"Website Contact: {form.subject}"
            
            body = f"""
New contact form submission:

Name: {form.name}
Email: {form.email}
Phone: {form.phone}
Subject: {form.subject}

Message:
{form.message}
"""
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            with smtplib.SMTP(current_app.config['MAIL_SERVER'], current_app.config['MAIL_PORT']) as server:
                if current_app.config['MAIL_USE_TLS']:
                    server.starttls()
                if current_app.config['MAIL_USERNAME']:
                    server.login(current_app.config['MAIL_USERNAME'], current_app.config['MAIL_PASSWORD'])
                server.send_message(msg)
        else:
            # Development mode - just log
            print(f"Contact form submission: {form.to_dict()}")
        
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

@main_bp.route('/api/services')
def api_services():
    """API endpoint for services"""
    return jsonify(SERVICES)

@main_bp.route('/api/testimonials')
def api_testimonials():
    """API endpoint for testimonials"""
    return jsonify(TESTIMONIALS)

@main_bp.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@main_bp.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return render_template('500.html'), 500
