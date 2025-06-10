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

### Step 2: Use IconField in your model

```python
from django.db import models
from django_icon_picker.field import IconField

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

    def __str__(self):
        return self.name
```

## Emoji Support

The emoji picker includes **80+ emojis** organized across categories:

- **😀 Smileys & People**: Happy, sad, thinking, party faces and hand gestures  
- **❤️ Hearts & Love**: Various colored hearts and love symbols
- **🎉 Activities**: Party, celebrations, sports, and entertainment
- **🌟 Symbols**: Stars, checkmarks, warnings, and common symbols  

### Search Examples:
- Type **"happy"** → finds 😀, 😃, 😊, 🥳
- Type **"heart"** → finds ❤️, 💙, 💚, 💛
- Type **"fire"** → finds 🔥

## User Interface

### Mode Toggle
- **🎨 Icons**: Search thousands of Iconify icons
- **😀 Emojis**: Browse curated emoji collection

### Keyboard Shortcuts
- **Alt + I**: Switch to icon mode
- **Alt + E**: Switch to emoji mode

## License

This project is licensed under the MIT License.

## Conclusion

Django Icon Picker with Emoji Support provides a comprehensive solution for adding visual elements to your Django applications. Whether you need scalable vector icons or expressive emojis, this package has you covered.
