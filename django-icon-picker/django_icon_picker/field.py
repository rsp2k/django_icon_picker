# fields.py
from django.db import models
from .widgets import IconPicker
from django.db.models.signals import pre_delete
from django.utils.html import format_html
import os
import re


class IconField(models.CharField):
    description = "A custom field to store icon information, supporting both SVG icons and text emojis."

    def __init__(self, *args, **kwargs):
        # Set default max_length to handle Unicode emojis and icon names
        kwargs["max_length"] = kwargs.get("max_length", 255)
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        widget = kwargs.get('widget')
        attrs = widget().attrs if widget else {}
        attrs.update({"model_name": self.model.__name__.lower()})
        kwargs["widget"] = IconPicker(attrs=attrs)
        return super().formfield(**kwargs)

    def contribute_to_class(self, cls, name, **kwargs):
        super().contribute_to_class(cls, name, **kwargs)
        pre_delete.connect(self._delete_file, sender=cls)

    def _delete_file(self, sender, instance, **kwargs):
        """Only delete SVG files, not emoji values"""
        file_path = getattr(instance, self.attname)
        if file_path and self.is_svg_file_path(file_path) and os.path.exists(file_path):
            try:
                os.remove(file_path)
            except OSError:
                pass

    def is_emoji(self, value):
        """Check if the value is an emoji"""
        if not value:
            return False
        # Unicode ranges for emojis
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
        """Check if the value is an icon name (like 'mdi:home')"""
        return value and isinstance(value, str) and ':' in value and not self.is_emoji(value)

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
        This is a helper method for use in templates or admin.
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
            return format_html(
                '<img src="https://api.iconify.design/{}.svg" class="icon-display {}" style="width: 1.2em; height: 1.2em; {}" alt="{}"/>',
                value,
                css_class,
                style,
                alt_text or f"Icon: {value}"
            )
        else:
            return format_html('<span class="icon-unknown {}" style="{}">{}</span>', css_class, style, value)

    def to_python(self, value):
        """Convert the value to a Python string, handling Unicode properly"""
        if value is None:
            return value
        return str(value)

    def get_prep_value(self, value):
        """Prepare the value for saving to the database"""
        if value is None:
            return value
        return str(value)
