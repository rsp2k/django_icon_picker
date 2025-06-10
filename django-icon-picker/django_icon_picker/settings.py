# django-icon-picker/django_icon_picker/settings.py
from django.conf import settings

# Default icon sets configuration
DEFAULT_ICON_SETS = [
    ('fontawesome5regular', 'far', 'Font Awesome 5 Regular', 'latest'),
    ('fontawesome5solid', 'fas', 'Font Awesome 5 Solid', 'latest'),
    ('fontawesome5brands', 'fab', 'Font Awesome 5 Brands', 'latest'),
    ('materialdesign', 'zmdi', 'Material Design'),
    ('ionicons', 'ion', 'Ionicons Icons'),
    ('octicons', 'octicon', 'Octicons'),
    ('typicons', 'typcn', 'Typicons'),
    ('weathericons', 'wi', 'Weather Icons'),
    ('glyphicons', 'glyphicon', 'Glyphicons'),
]

# User can override this in their Django settings
ICON_SETS = getattr(settings, 'DJANGO_ICON_SETS', DEFAULT_ICON_SETS)

# Default icon color
ICON_COLOR = getattr(settings, 'ICON_PICKER_COLOR', '#00bcc9')

# Path for SVG icon storage (optional)
ICON_PICKER_PATH = getattr(settings, 'ICON_PICKER_PATH', None)

# Template choices for different icon rendering styles
ICON_TEMPLATES = getattr(settings, 'DJANGO_ICON_TEMPLATES', [
    ('default', 'Default Template'),
    ('svg', 'SVG Template'),
    ('custom', 'Custom Template'),
])

# Advanced settings
ICON_PICKER_SETTINGS = getattr(settings, 'ICON_PICKER_SETTINGS', {
    'search_enabled': True,
    'categories_enabled': True,
    'recent_icons_enabled': True,
    'favorites_enabled': True,
    'preview_enabled': True,
    'lazy_loading': True,
    'icons_per_page': 50,
    'search_debounce': 300,  # milliseconds
})

# CDN URLs for different icon libraries
ICON_CDN_URLS = getattr(settings, 'ICON_CDN_URLS', {
    'fontawesome5': 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css',
    'fontawesome6': 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css',
    'materialdesign': 'https://cdnjs.cloudflare.com/ajax/libs/material-design-iconic-font/2.2.0/css/material-design-iconic-font.min.css',
    'ionicons': 'https://cdnjs.cloudflare.com/ajax/libs/ionicons/6.0.3/collection/components/icon/icon.min.js',
    'octicons': 'https://cdnjs.cloudflare.com/ajax/libs/octicons/17.3.0/font/octicons.css',
    'typicons': 'https://cdnjs.cloudflare.com/ajax/libs/typicons/2.1.2/typicons.min.css',
    'weathericons': 'https://cdnjs.cloudflare.com/ajax/libs/weather-icons/2.0.12/css/weather-icons.min.css',
})
