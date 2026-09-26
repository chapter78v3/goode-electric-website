"""Data models for Goode Electric website"""
import re

# Service Categories
SERVICES = [
    {
        'id': 1,
        'category': 'Core Maintenance & Repairs',
        'description': 'Keep your electrical system running smoothly with professional maintenance and repair services.',
        'items': [
            'Troubleshooting: Finding out why lights flicker, power goes out, or breakers trip',
            'Outlet and Switch Repair: Fixing loose plugs, broken switches, and warm outlets',
            'Breaker Replacement: Swapping out old or broken circuit breakers in the main panel'
        ]
    },
    {
        'id': 2,
        'category': 'New Installations',
        'description': 'Expand your home\'s functionality with expert installation of modern electrical systems.',
        'items': [
            'Lighting Fixtures: Hanging chandeliers, recessed lights, track lighting, and outdoor security lights',
            'Ceiling Fans: Wiring and mounting fans in bedrooms, living rooms, and patios',
            'Smart Home Devices: Installing smart doorbells, thermostats, security cameras, and automated switches',
            'Appliance Wiring: Setting up dedicated lines for heavy appliances like dryers, ovens, and hot tubs',
            'EV Charging Stations: Installing Level 2 electric vehicle chargers in garages or driveways'
        ]
    },
    {
        'id': 3,
        'category': 'System Upgrades & Safety',
        'description': 'Ensure your home meets modern safety standards with comprehensive electrical system upgrades.',
        'items': [
            'Panel Upgrades: Replacing old electrical panels to safely handle more modern appliances',
            'Whole-House Rewiring: Removing outdated, dangerous wiring like knob-and-tube or aluminum cables',
            'Surge Protection: Installing a main surge protector at the panel to shield electronics from lightning spikes',
            'Safety Inspections: Checking a home\'s electrical system to ensure it passes local building safety codes',
            'Smoke Detectors: Hardwiring interconnected smoke and carbon monoxide alarms throughout a building'
        ]
    }
]

# Customer Testimonials
TESTIMONIALS = [
    {
        'id': 1,
        'name': 'John Smith',
        'text': 'Goode Electric provided excellent service when our breaker panel needed replacement. The team was professional, efficient, and explained everything clearly. Highly recommend!',
        'rating': 5
    },
    {
        'id': 2,
        'name': 'Sarah Johnson',
        'text': 'We had them install EV charging stations at our home. The work was done perfectly and they made sure everything was up to code. Great experience!',
        'rating': 5
    },
    {
        'id': 3,
        'name': 'Michael Brown',
        'text': 'Called them for a troubleshooting issue with flickering lights. They diagnosed the problem quickly and had it fixed the same day. Fast and reliable service.',
        'rating': 5
    },
    {
        'id': 4,
        'name': 'Emily Davis',
        'text': 'Had them do our whole-house rewiring. Professional team, great communication, and the quality of work is outstanding. Worth every penny!',
        'rating': 5
    },
    {
        'id': 5,
        'name': 'Robert Wilson',
        'text': 'Excellent customer service! They came out for a safety inspection and found several issues. Fixed them all properly and took time to educate us.',
        'rating': 5
    },
    {
        'id': 6,
        'name': 'Jessica Martinez',
        'text': 'Had smart home devices installed. The team was knowledgeable, courteous, and everything works perfectly. Would definitely use them again!',
        'rating': 5
    }
]

class ContactForm:
    """Model for contact form submissions"""

    # Upper bounds on every field. Without these a single request could carry
    # megabytes of text into an outbound email and into the logs.
    MAX_LENGTHS = {
        'name': 100,
        'email': 254,      # RFC 5321 maximum address length
        'phone': 32,
        'subject': 200,
        'message': 5000,
    }
    MIN_MESSAGE_LENGTH = 10
    # Deliberately permissive: enough to reject junk that would make ACS
    # reject the whole send, without policing exotic but legal addresses.
    EMAIL_RE = re.compile(r'^[^@\s]+@[^@\s.]+(\.[^@\s.]+)+$')

    def __init__(self, name, email, phone, subject, message):
        self.name = name
        self.email = email
        self.phone = phone
        self.subject = subject
        self.message = message

    def validation_error(self):
        """Return a human-readable reason the form is invalid, or None."""
        fields = {
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'subject': self.subject,
            'message': self.message,
        }
        for field, value in fields.items():
            if not value:
                return 'Please fill in all fields correctly'
            if len(value) > self.MAX_LENGTHS[field]:
                return f'{field.capitalize()} is too long (max {self.MAX_LENGTHS[field]} characters)'
        if len(self.message) <= self.MIN_MESSAGE_LENGTH:
            return 'Please provide a longer message'
        if not self.EMAIL_RE.match(self.email):
            return 'Please enter a valid email address'
        return None

    def is_valid(self):
        """Validate form data"""
        return self.validation_error() is None


    def to_dict(self):
        """Convert to dictionary"""
        return {
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'subject': self.subject,
            'message': self.message
        }

# Rename 'items' key to 'service_items' to avoid conflicts with dict.items() method
# Apply fix by accessing with bracket notation in templates
