# Goode Electric Website - Development Instructions

## Project Overview
- **Client**: Goode Electric (Electrician company, Birmingham, AL)
- **Tech Stack**: Python Flask, Bootstrap 5, HTML/CSS/JavaScript
- **Timeline**: MVP in 2 weeks
- **Hosting**: GitHub (code) & Azure App Service (web app)

## Quick Start

### Setup (First Time)
1. Navigate to project root
2. Create virtual environment: `python -m venv venv`
3. Activate venv: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux)
4. Install dependencies: `pip install -r requirements.txt`
5. Run app: `python run.py`
6. Open browser to `http://localhost:5000`

### Modify Content
- **Services**: Edit `app/models.py` > `SERVICES` list
- **Testimonials**: Edit `app/models.py` > `TESTIMONIALS` list
- **Pages**: Modify HTML in `app/templates/` and add routes in `app/routes.py`

### Style Customization
- Color scheme in `app/static/css/style.css`
- Bootstrap classes in HTML templates
- Primary colors: Orange (#F59E0B), Warm Yellow (#FCD34D)

## Project Structure
```
goode-electric-website/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── models.py            # Services & testimonials data
│   ├── routes.py            # URL routes & logic
│   ├── templates/           # HTML templates
│   └── static/css/          # CSS styling
├── run.py                   # Start the app
├── config.py                # Configuration
├── requirements.txt         # Dependencies
└── README.md                # Documentation
```

## Key Files

### Models (`app/models.py`)
- `SERVICES`: Array of 3 service categories with descriptions and items
- `TESTIMONIALS`: Array of customer testimonials with ratings
- `ContactForm`: Class for form validation

### Routes (`app/routes.py`)
- `/` - Homepage
- `/services` - Services page
- `/testimonials` - Testimonials page
- `/contact` - Contact form (GET/POST)
- `/api/services` - JSON API
- `/api/testimonials` - JSON API

### Templates (`app/templates/`)
- `base.html` - Navigation & footer
- `index.html` - Homepage with hero section
- `services.html` - Service categories
- `testimonials.html` - Customer reviews
- `contact.html` - Contact form
- `404.html`, `500.html` - Error pages

## Common Tasks

### Add New Service
1. Open `app/models.py`
2. Add item to SERVICES array:
```python
{
    'id': 4,
    'category': 'New Category',
    'description': 'Description here',
    'items': ['Item 1', 'Item 2']
}
```

### Add Testimonial
1. Open `app/models.py`
2. Add to TESTIMONIALS array:
```python
{
    'id': 7,
    'name': 'Customer Name',
    'text': 'Testimonial text here',
    'rating': 5
}
```

### Create New Page
1. Create template in `app/templates/newpage.html`
2. Add route in `app/routes.py`:
```python
@main_bp.route('/newpage')
def newpage():
    return render_template('newpage.html')
```

## Azure Deployment Checklist
- [ ] Set `FLASK_ENV=production`
- [ ] Configure environment variables
- [ ] Enable HTTPS
- [ ] Set up email (SMTP)
- [ ] Test contact form
- [ ] Verify all pages load correctly
- [ ] Test mobile responsiveness

## Debugging
- **Port conflict**: Use `python -m flask run --port 5001`
- **Module errors**: Ensure venv is activated and requirements installed
- **Template errors**: Check `app/templates/` file names and route definitions
- **Email issues**: Verify `.env` SMTP credentials and firewall settings

## Next Steps for Full Site
1. Add service images/gallery
2. Implement online booking system
3. Add admin dashboard for content management
4. Set up payment processing
5. Add blog/news section
6. Integrate Google Maps for service area

## Contact
For issues or questions: support@chappellsecuretec.com

---
Generated: August 2024
