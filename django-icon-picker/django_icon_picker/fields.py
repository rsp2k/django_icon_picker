# django-icon-picker/django_icon_picker/fields.py
import json
import os
from django import forms
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.html import format_html
from django.conf import settings
from .widgets import IconPickerWidget
from .settings import ICON_SETS, ICON_PICKER_PATH
from .utils import download_svg_icon, validate_icon_format


class IconField(models.CharField):
    """
    Enhanced icon field that supports multiple icon libraries,
    SVG icons, emojis, and advanced configuration options.
    
    This field maintains backward compatibility with the original
    emoji/SVG functionality while adding support for Font Awesome,
    Material Design, and other icon libraries.
    """
    
    def __init__(self, icon_set=None, template='default', allow_svg=True, 
                 allow_custom=True, allow_emoji=True, required_prefix=None, *args, **kwargs):
        """
        Initialize the IconField with enhanced options.
        
        Args:
            icon_set: Specific icon set to use (if None, uses all available)
            template: Template style for rendering icons
            allow_svg: Whether to allow SVG icon uploads
            allow_custom: Whether to allow custom icon inputs
            allow_emoji: Whether to allow emoji selection (backward compatibility)
            required_prefix: Required prefix for icon names (e.g., 'fa-')
        """
        self.icon_set = icon_set
        self.template = template
        self.allow_svg = allow_svg
        self.allow_custom = allow_custom
        self.allow_emoji = allow_emoji
        self.required_prefix = required_prefix
        
        kwargs.setdefault('max_length', 255)
        super().__init__(*args, **kwargs)
    
    def formfield(self, **kwargs):
        """Return the form field for this model field."""
        defaults = {
            'widget': IconPickerWidget(
                icon_set=self.icon_set,
                template=self.template,
                allow_svg=self.allow_svg,
                allow_custom=self.allow_custom,
                allow_emoji=self.allow_emoji,
                required_prefix=self.required_prefix,
            ),
            'form_class': IconFormField,
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)
    
    def validate(self, value, model_instance):
        """Validate the icon value."""
        super().validate(value, model_instance)
        
        if value and self.required_prefix:
            if not value.startswith(self.required_prefix):
                raise ValidationError(
                    f'Icon must start with prefix: {self.required_prefix}'
                )
        
        if value and not validate_icon_format(value):
            raise ValidationError('Invalid icon format')
    
    # Backward compatibility methods from original field
    def is_emoji(self, value):
        """Check if the value is an emoji"""
        if not value:
            return False
        # Unicode ranges for emojis
        import re
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F1E0-\U0001F1FF"  # flags (iOS)
            "\U00002600-\U000026FF"  # miscellaneous symbols
            "\U00002700-\U000027BF"  # dingbats
            "\U0001F900-\U0001F9FF"  # supplemental symbols
            "\U0001FA70-\U0001FAFF"  # symbols and pictographs extended-a
            "]+",
            flags=re.UNICODE
        )
        return bool(emoji_pattern.search(value))
    
    def is_svg_file_path(self, value):
        """Check if the value is a file path to an SVG"""
        return value and isinstance(value, str) and value.endswith('.svg') and '/' in value
    
    def is_icon_name(self, value):
        """Check if the value is an icon name (like 'mdi:home' or 'fas fa-home')"""
        if not value or not isinstance(value, str):
            return False
        # Font Awesome style
        if any(value.startswith(prefix) for prefix in ['fas ', 'far ', 'fab ', 'fal ']):
            return True
        # Iconify style
        return ':' in value and not self.is_emoji(value)
    
    def get_icon_type(self, value):
        """Determine the type of icon value"""
        if not value:
            return 'none'
        elif self.is_emoji(value):
            return 'emoji'
        elif self.is_svg_file_path(value):
            return 'svg_file'
        elif self.is_icon_name(value):
            return 'icon_name'
        else:
            return 'unknown'
    
    def get_display_html(self, value, css_class="", style="", alt_text=""):
        """
        Get HTML representation of the icon value.
        This method provides backward compatibility while supporting new icon types.
        """
        if not value:
            return ""

        icon_type = self.get_icon_type(value)
        
        if icon_type == 'emoji':
            return format_html(
                '<span class="emoji-display {}" style="font-size: 1.2em; {}" title="{}">{}</span>',
                css_class,
                style,
                alt_text or f"Emoji: {value}",
                value
            )
        elif icon_type == 'svg_file':
            return format_html(
                '<img src="{}" class="icon-display {}" style="width: 1.2em; height: 1.2em; {}" alt="{}"/>',
                f"/{value}",
                css_class,
                style,
                alt_text or "Icon"
            )
        elif icon_type == 'icon_name':
            # Handle both Iconify and Font Awesome formats
            if ':' in value:
                # Iconify format (mdi:home)
                return format_html(
                    '<img src="https://api.iconify.design/{}.svg" class="icon-display {}" style="width: 1.2em; height: 1.2em; {}" alt="{}"/>',
                    value,
                    css_class,
                    style,
                    alt_text or f"Icon: {value}"
                )
            else:
                # Font Awesome format (fas fa-home)
                return format_html(
                    '<i class="{} icon-display {}" style="{}" title="{}"></i>',
                    value,
                    css_class,
                    style,
                    alt_text or f"Icon: {value}"
                )
        else:
            return format_html('<span class="icon-unknown {}" style="{}">{}</span>', css_class, style, value)


class IconFormField(forms.CharField):
    """Form field for icon selection with enhanced validation."""
    
    def __init__(self, icon_set=None, template='default', allow_svg=True,
                 allow_custom=True, allow_emoji=True, required_prefix=None, *args, **kwargs):
        self.icon_set = icon_set
        self.template = template
        self.allow_svg = allow_svg
        self.allow_custom = allow_custom
        self.allow_emoji = allow_emoji
        self.required_prefix = required_prefix
        
        super().__init__(*args, **kwargs)
        
        self.widget = IconPickerWidget(
            icon_set=icon_set,
            template=template,
            allow_svg=allow_svg,
            allow_custom=allow_custom,
            allow_emoji=allow_emoji,
            required_prefix=required_prefix,
        )
    
    def clean(self, value):
        """Clean and validate the icon value."""
        value = super().clean(value)
        
        if value:
            # Handle SVG file upload if enabled
            if self.allow_svg and value.endswith('.svg') and ICON_PICKER_PATH:
                try:
                    # Download and save SVG if it's a URL
                    if value.startswith(('http://', 'https://')):
                        local_path = download_svg_icon(value, ICON_PICKER_PATH)
                        value = local_path
                except Exception as e:
                    raise ValidationError(f'Failed to process SVG icon: {e}')
            
            # Validate prefix requirement
            if self.required_prefix and not value.startswith(self.required_prefix):
                raise ValidationError(
                    f'Icon must start with prefix: {self.required_prefix}'
                )
            
            # Validate icon format
            if not validate_icon_format(value):
                raise ValidationError('Invalid icon format')
        
        return value


class IconChoiceField(forms.ChoiceField):
    """Choice field for selecting from predefined icon sets."""
    
    def __init__(self, icon_set=None, *args, **kwargs):
        self.icon_set = icon_set or 'fontawesome5solid'
        
        # Generate choices from icon set
        choices = self._get_icon_choices()
        kwargs['choices'] = choices
        
        super().__init__(*args, **kwargs)
        self.widget = IconPickerWidget(icon_set=self.icon_set)
    
    def _get_icon_choices(self):
        """Generate choices from the specified icon set."""
        # This would be populated from icon data files
        return [
            ('', '-- Select an icon --'),
            ('fas fa-home', 'Home'),
            ('fas fa-user', 'User'),
            ('fas fa-search', 'Search'),
            ('fas fa-cog', 'Settings'),
            ('fas fa-heart', 'Heart'),
        ]


class SVGIconField(models.FileField):
    """Specialized field for SVG icon uploads."""
    
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('upload_to', 'icons/svg/')
        super().__init__(*args, **kwargs)
    
    def clean(self, *args, **kwargs):
        """Validate that uploaded file is a valid SVG."""
        data = super().clean(*args, **kwargs)
        
        if data:
            if not data.name.lower().endswith('.svg'):
                raise ValidationError('Only SVG files are allowed.')
            
            # Additional SVG validation could be added here
        
        return data


# Utility function for easy icon rendering in templates
def render_icon(icon_value, css_classes='', attributes=None, template='default'):
    """
    Render an icon with the specified template and attributes.
    
    Args:
        icon_value: The icon identifier (class name, file path, emoji, etc.)
        css_classes: Additional CSS classes to apply
        attributes: Dictionary of HTML attributes
        template: Template style to use for rendering
    
    Returns:
        HTML string for the rendered icon
    """
    if not icon_value:
        return ""
    
    attributes = attributes or {}
    
    # Create a temporary field instance to use its methods
    field = IconField()
    
    return field.get_display_html(
        icon_value, 
        css_class=css_classes,
        style=attributes.get('style', ''),
        alt_text=attributes.get('alt', '')
    )
