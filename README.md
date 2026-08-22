# Goode Electric - Website

A professional, responsive website for Goode Electric, a Birmingham, AL-based electrician company. Built with Flask, Bootstrap, and modern web technologies.

## Features

- **Responsive Design** - Mobile-friendly interface using Bootstrap 5
- **Service Portfolio** - Showcase of services across three categories
- **Testimonials** - Display of customer reviews and ratings
- **Contact Form** - Email submission form for customer inquiries
- **Service Area Map** - Birmingham, AL metro area coverage
- **Professional Styling** - Warm, welcoming color scheme (orange/amber tones)

## Project Structure

```
goode-electric-website/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── models.py            # Data models (services, testimonials)
│   ├── routes.py            # Route definitions and logic
│   ├── templates/
│   │   ├── base.html        # Base template with navigation/footer
│   │   ├── index.html       # Homepage
│   │   ├── services.html    # Services page
│   │   ├── testimonials.html # Testimonials page
│   │   ├── contact.html     # Contact form
│   │   ├── 404.html         # 404 error page
│   │   └── 500.html         # 500 error page
│   └── static/
│       └── css/
│           └── style.css    # Custom styling
├── run.py                   # Application entry point
├── config.py                # Configuration management
├── requirements.txt         # Python dependencies
├── .gitignore               # Git ignore rules
├── .env.example             # Example environment variables
└── README.md                # This file
```

## Tech Stack

- **Backend**: Flask 3.0.0 (Python web framework)
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Styling**: Bootstrap & custom CSS with warm color theme
- **Email**: Flask-Mail for contact form submissions
- **Environment**: python-dotenv for configuration

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/ChappellSecureSolutions/goode-electric-website.git
   cd goode-electric-website
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**
   - **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Create `.env` file** (optional for local development)
   ```bash
   cp .env.example .env
   ```

6. **Run the application**
   ```bash
   python run.py
   ```

7. **Access the application**
   - Open your browser and navigate to `http://localhost:5000`

## Configuration

Create a `.env` file in the project root with the following environment variables:

```env
# Flask Configuration
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

# Email Configuration (optional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=noreply@goodeelectric.com
RECIPIENT_EMAIL=contact@goodeelectric.com

# Google Maps API (optional, for future integration)
MAPS_API_KEY=your-google-maps-api-key
```

## Features Overview

### Homepage
- Hero section with call-to-action
- Service category preview
- Featured testimonials
- Professional design with warm colors

### Services Page
- Detailed breakdown of three service categories
- Service area information
- Operating hours and emergency availability

### Testimonials Page
- Full list of customer testimonials
- 5-star ratings
- Customer statistics
- Call-to-action for new customers

### Contact Form
- Full-name, email, phone, subject, and message fields
- Form validation
- Email submission (when configured)
- Success/error messaging

## Deployment

### Azure App Service

1. **Install Azure CLI**
   ```bash
   # Instructions at https://learn.microsoft.com/en-us/cli/azure/install-azure-cli
   ```

2. **Create Resource Group**
   ```bash
   az group create --name goode-electric-rg --location eastus
   ```

3. **Create App Service Plan**
   ```bash
   az appservice plan create --name goode-electric-plan --resource-group goode-electric-rg --sku B1 --is-linux
   ```

4. **Create Web App**
   ```bash
   az webapp create --resource-group goode-electric-rg --plan goode-electric-plan --name goode-electric --runtime "PYTHON|3.11"
   ```

5. **Deploy from GitHub**
   - Connect your GitHub repository to Azure App Service
   - Enable continuous deployment

6. **Configure Environment Variables**
   - Set all `.env` variables in Azure App Service Configuration

### Docker Deployment

A Dockerfile can be created for containerized deployment. Contact your development team for Docker setup.

## GitHub Repository Setup

1. **Initialize Git**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Goode Electric website"
   ```

2. **Add Remote**
   ```bash
   git remote add origin https://github.com/ChappellSecureSolutions/goode-electric-website.git
   git branch -M main
   git push -u origin main
   ```

## Development Workflow

### Adding New Content

**Services**: Edit `app/models.py` - Update the `SERVICES` list

**Testimonials**: Edit `app/models.py` - Update the `TESTIMONIALS` list

**Pages**: Create new HTML templates in `app/templates/` and add corresponding routes in `app/routes.py`

### Testing

```bash
# Run Flask development server with debugging
FLASK_ENV=development python run.py

# Application will be available at http://localhost:5000
```

## Customization

### Color Scheme
Edit `app/static/css/style.css` to modify the color palette:
- Primary Orange: `#F59E0B`
- Dark Orange: `#D97706`
- Warm Yellow: `#FCD34D`

### Branding
- Update company name, phone, email in templates and routes
- Replace or update images in `app/static/`
- Customize footer information in `app/templates/base.html`

## Email Configuration

For production, configure SMTP settings:
- Gmail: Use App Passwords with Gmail account
- Office 365: Use your organizational email settings
- SendGrid/Mailgun: Use their SMTP servers

## Security Considerations

1. **Environment Variables**: Never commit `.env` file to repository
2. **Secret Key**: Use a strong, random secret key in production
3. **HTTPS**: Enable SSL/TLS in production
4. **Form Validation**: All form inputs are validated server-side
5. **Email Verification**: Consider adding email verification for contact submissions

## Troubleshooting

### Port Already in Use
```bash
# Use a different port
python -m flask run --port 5001
```

### Module Not Found
```bash
# Ensure virtual environment is activated and dependencies installed
pip install -r requirements.txt
```

### Email Not Sending
- Verify SMTP credentials in `.env`
- Check firewall/network permissions
- Enable "Less secure app access" for Gmail (if applicable)

## Support & Maintenance

For questions or issues:
- Contact: Chappell Secure Technology Solutions
- Email: support@chappellsecuretec.com

## Future Enhancements

- [ ] Online booking system
- [ ] Photo gallery for completed projects
- [ ] Blog/news section
- [ ] Integration with Google Maps
- [ ] Admin dashboard for content management
- [ ] Customer portal
- [ ] Payment processing
- [ ] Multi-language support

## License

© 2024 Goode Electric. All rights reserved.

---

**Last Updated**: August 2024
