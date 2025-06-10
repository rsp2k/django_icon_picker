# Django Icon Picker with Emoji Support

## Overview

Django Icon Picker is a custom Django model field that allows users to select icons from a predefined set **or choose from a curated collection of emojis**. It supports SVG icons, icon IDs, and text emojis, depending on the configuration.

## Features

- **🎨 SVG Icon Support**: Download and save SVG files from Iconify API with customizable colors
- **😀 Text Emoji Support**: Choose from 80+ carefully curated emojis across multiple categories
- **🔄 Dual Mode Interface**: Easy toggle between icon and emoji modes
- **🎯 Smart Search**: Search icons by name or emojis by name/keywords (e.g., "happy", "heart", "fire")
- **🎨 Color Customization**: Full color control for SVG icons (emojis use their natural colors)
- **📱 Responsive Design**: Works seamlessly on desktop and mobile devices
- **♿ Accessibility**: Full ARIA support and keyboard navigation
- **🌙 Dark Mode**: Built-in dark theme support

## Screenshot

![Django Icon Picker Demo](icon_picker.gif)

## Installation & Usage

### Step 1: Install Django Icon Picker

```bash
pip install django-icon-picker
```

Add `django_icon_picker` to `INSTALLED_APPS`:

```python
# settings.py
INSTALLED_APPS = [
    # Other installed apps...
    'django_icon_picker',
]
```

Update `urls.py` (required for SVG file download functionality):

```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("icon_picker/", include("django_icon_picker.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### Step 2: Configure Django Settings

```python
# settings.py

# Optional: Path where SVG files will be saved (for icon mode)
ICON_PICKER_PATH = 'media'

# Default icon color
ICON_PICKER_COLOR = "#00bcc9"
```

### Step 3: Use IconField in your model

```python
from django.db import models
from django_icon_picker.field import IconField
from django.utils.html import format_html

class ExampleModel(models.Model):
    icon = IconField(max_length=255)
    name = models.CharField(max_length=255)

    def display_icon(self):
        """Display the icon/emoji with proper formatting"""
        return self.icon.get_display_html(
            css_class="model-icon",
            style="margin-right: 8px;",
            alt_text=f"Icon for {self.name}"
        )
    
    def icon_type(self):
        """Get the type of icon stored"""
        return self.icon.get_icon_type(self.icon)

    def __str__(self):
        return self.name
```

## Emoji Categories & Search

The emoji picker includes **80+ emojis** organized across categories:

- **😀 Smileys & People**: Happy, sad, thinking, party faces and hand gestures  
- **❤️ Hearts & Love**: Various colored hearts and love symbols
- **🎉 Activities**: Party, celebrations, sports, and entertainment
- **🔥 Symbols**: Stars, checkmarks, warnings, and common symbols  
- **📱 Objects**: Technology, tools, communication devices
- **🌈 Nature**: Weather, plants, celestial objects
- **🍕 Food & Drink**: Popular foods, beverages, and treats
- **🚀 Transport**: Vehicles, travel, and movement

### Search Examples:
- Type **"happy"** ➔ finds 😀, 😃, 😊, 🥳
- Type **"heart"** ➔ finds ❤️, 💙, 💚, 💜, 🧡, 💛
- Type **"fire"** ➔ finds 🔥
- Type **"star"** ➔ finds ⭐, 🌟, ✨

## User Interface

### Mode Toggle
- **🎨 Icons**: Search and select from thousands of Iconify icons
- **😀 Emojis**: Browse curated emoji collection with keyword search

### Keyboard Shortcuts
- **Alt + I**: Switch to icon mode
- **Alt + E**: Switch to emoji mode

### Smart Features
- **Auto-detection**: Automatically detects if stored value is emoji or icon
- **Color picker**: Only shows for icon mode (emojis use natural colors)
- **Live preview**: See selected icon/emoji instantly
- **Responsive search**: Real-time results as you type

## Field Methods

The `IconField` provides helpful methods:

```python
# Check what type of value is stored
model_instance.icon.get_icon_type()  # Returns: 'emoji', 'icon_name', 'svg_file', or 'none'

# Get HTML representation for templates
model_instance.icon.get_display_html(css_class="my-icon", style="font-size: 2em;")

# Check specific types
model_instance.icon.is_emoji()        # True if emoji
model_instance.icon.is_svg_file_path() # True if SVG file path
model_instance.icon.is_icon_name()    # True if icon name (like 'mdi:home')
```

## Template Usage

```html
<!-- Display icon/emoji in templates -->
<div class="item">
    {{ object.display_icon|safe }}
    <span>{{ object.name }}</span>
</div>

<!-- Or use the field method directly -->
<div class="item">
    {{ object.icon.get_display_html:"item-icon":"font-size: 1.5em;"|safe }}
    <span>{{ object.name }}</span>
</div>
```

## Testing & Development

### Test Fixtures

The example project includes comprehensive test fixtures to demonstrate the icon picker:

```bash
cd django_icon_picker_example

# Load comprehensive test data (40 diverse icons)
python manage.py load_test_data

# Load specific fixture sets
python manage.py load_test_data --fixture=basic_icons
python manage.py load_test_data --fixture=brand_icons
python manage.py load_test_data --fixture=heroicons

# Clear and reload data
python manage.py load_test_data --clear

# Verify existing data
python manage.py load_test_data --verify-only
```

**Available Test Fixtures:**
- `comprehensive_test_data.json` - 40 diverse icons across multiple icon sets
- `basic_icons.json` - 15 Material Symbols icons for common UI elements
- `brand_icons.json` - 10 Font Awesome brand icons for social platforms
- `heroicons.json` - 10 modern outline-style icons

### Icon Sets Demonstrated

- **Material Symbols**: `material-symbols:home`, `material-symbols:settings`
- **Font Awesome**: `fa-brands:github`, `fa-brands:twitter`
- **Heroicons**: `heroicons:academic-cap`, `heroicons:camera`
- **Material Design Icons**: `mdi:weather-sunny`, `mdi:heart`

### Automated Testing

The repository includes GitHub Actions that:
- ✅ Run comprehensive Django tests across Python 3.9-3.12 and Django 4.2-5.1
- 📸 Take automated screenshots of the admin interface
- 🔍 Capture detailed DEBUG logs during testing
- 📦 Save screenshots and logs as downloadable artifacts
- 🎯 Load test fixtures for realistic demo data

## Configuration Options

| Setting | Default | Description |
|---------|---------|-------------|
| `ICON_PICKER_PATH` | `None` | Path where SVG files will be saved. If not defined, only icon IDs are stored. |
| `ICON_PICKER_COLOR` | `"#00bcc9"` | Default color for icons (doesn't affect emojis) |

## Browser Support

- **Modern browsers**: Chrome 60+, Firefox 55+, Safari 10+, Edge 79+
- **Mobile**: iOS Safari 10+, Chrome Mobile 60+
- **Emoji support**: Native emoji rendering on all modern platforms

## Requirements

- Django >= 3.0
- Python >= 3.6
- Modern web browser with JavaScript enabled

## Accessibility

- **ARIA labels**: Full screen reader support
- **Keyboard navigation**: Tab through all interface elements
- **High contrast**: Supports high contrast mode
- **Focus indicators**: Clear focus states for all interactive elements

## Contributing

Contributions are welcome! Areas for improvement:
- Additional emoji categories
- Icon pack integration
- Custom emoji upload
- Advanced search filters
- Improved test coverage
- Enhanced screenshot testing

## License

This project is licensed under the MIT License.

## Conclusion

Django Icon Picker with Emoji Support provides a comprehensive solution for adding visual elements to your Django applications. Whether you need scalable vector icons or expressive emojis, this package has you covered with an intuitive, accessible interface.
