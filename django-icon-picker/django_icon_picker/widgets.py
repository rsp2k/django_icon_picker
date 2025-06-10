# django-icon-picker/django_icon_picker/widgets.py
import json
from django import forms
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.templatetags.static import static
from django.urls import reverse
from .settings import ICON_SETS, ICON_COLOR, ICON_PICKER_SETTINGS


class IconPickerWidget(forms.TextInput):
    """
    Enhanced icon picker widget with support for multiple icon libraries,
    emojis, search functionality, favorites, and advanced features.
    
    Maintains backward compatibility with the original emoji/SVG functionality.
    """
    
    template_name = 'django_icon_picker/icon_picker_widget.html'
    
    def __init__(self, icon_set=None, template='default', allow_svg=True,
                 allow_custom=True, allow_emoji=True, required_prefix=None, attrs=None):
        self.icon_set = icon_set
        self.template = template
        self.allow_svg = allow_svg
        self.allow_custom = allow_custom
        self.allow_emoji = allow_emoji  # Backward compatibility
        self.required_prefix = required_prefix
        
        default_attrs = {
            'class': 'icon-picker-input',
            'readonly': 'readonly',
        }
        if attrs:
            default_attrs.update(attrs)
        
        super().__init__(attrs=default_attrs)
    
    def render(self, name, value, attrs=None, renderer=None):
        """Render the widget with enhanced UI."""
        if attrs is None:
            attrs = {}
        
        # Generate unique ID for this widget instance
        widget_id = attrs.get('id', f'icon_picker_{name}')
        
        # Prepare configuration data
        config = {
            'iconSets': self._get_available_icon_sets(),
            'selectedIconSet': self.icon_set or (ICON_SETS[0][0] if ICON_SETS else None),
            'allowSvg': self.allow_svg,
            'allowCustom': self.allow_custom,
            'allowEmoji': self.allow_emoji,  # Backward compatibility
            'requiredPrefix': self.required_prefix,
            'color': ICON_COLOR,
            'settings': ICON_PICKER_SETTINGS,
            'apiUrl': self._safe_reverse('icon_picker:api', '/icon_picker/api/'),
            'searchUrl': self._safe_reverse('icon_picker:search', '/icon_picker/search/'),
        }
        
        # Base input field
        input_html = super().render(name, value, attrs, renderer)
        
        # Icon preview
        preview_html = self._render_preview(value) if value else ''
        
        # Picker button and modal
        picker_html = f'''
        <div class="icon-picker-container" id="{widget_id}_container">
            <div class="icon-picker-input-group">
                {input_html}
                <div class="icon-picker-preview" id="{widget_id}_preview">
                    {preview_html}
                </div>
                <button type="button" class="icon-picker-button btn btn-outline-secondary" 
                        id="{widget_id}_button" data-target="#{widget_id}_modal">
                    🎨 Choose Icon
                </button>
                {'<button type="button" class="icon-picker-clear btn btn-outline-danger" id="' + widget_id + '_clear">✖</button>' if value else ''}
            </div>
            
            <!-- Icon Picker Modal -->
            <div class="icon-picker-modal" id="{widget_id}_modal" style="display: none;">
                <div class="icon-picker-modal-content">
                    <div class="icon-picker-header">
                        <h3>Choose an Icon</h3>
                        <button type="button" class="icon-picker-close" id="{widget_id}_close">
                            ✖
                        </button>
                    </div>
                    
                    <div class="icon-picker-toolbar">
                        <div class="icon-picker-search">
                            <input type="text" class="form-control" placeholder="Search icons..." 
                                   id="{widget_id}_search">
                            <span class="search-icon">🔍</span>
                        </div>
                        
                        <div class="icon-picker-filters">
                            <select class="form-control icon-set-selector" id="{widget_id}_iconset">
                                {self._render_icon_set_options()}
                            </select>
                            
                            <div class="icon-picker-view-options">
                                <button type="button" class="btn btn-sm view-grid active" title="Grid View">
                                    ⊞
                                </button>
                                <button type="button" class="btn btn-sm view-list" title="List View">
                                    ☰
                                </button>
                            </div>
                        </div>
                    </div>
                    
                    <div class="icon-picker-tabs">
                        <button type="button" class="tab-button active" data-tab="all">All Icons</button>
                        <button type="button" class="tab-button" data-tab="recent">Recent</button>
                        <button type="button" class="tab-button" data-tab="favorites">Favorites</button>
                        {f'<button type="button" class="tab-button" data-tab="emoji">Emojis</button>' if self.allow_emoji else ''}
                        {f'<button type="button" class="tab-button" data-tab="custom">Custom</button>' if self.allow_custom else ''}
                        {f'<button type="button" class="tab-button" data-tab="svg">SVG Upload</button>' if self.allow_svg else ''}
                    </div>
                    
                    <div class="icon-picker-content">
                        <div class="icon-picker-grid" id="{widget_id}_grid">
                            <!-- Icons will be loaded here via JavaScript -->
                        </div>
                        
                        <div class="icon-picker-pagination">
                            <button type="button" class="btn btn-sm btn-outline-secondary" id="{widget_id}_prev" disabled>
                                ← Previous
                            </button>
                            <span class="pagination-info" id="{widget_id}_info">Loading...</span>
                            <button type="button" class="btn btn-sm btn-outline-secondary" id="{widget_id}_next">
                                Next →
                            </button>
                        </div>
                    </div>
                    
                    <div class="icon-picker-footer">
                        <div class="selected-icon-info" id="{widget_id}_selected_info" style="display: none;">
                            <strong>Selected:</strong> <span class="selected-icon-name"></span>
                        </div>
                        <div class="icon-picker-actions">
                            <button type="button" class="btn btn-secondary" id="{widget_id}_cancel">Cancel</button>
                            <button type="button" class="btn btn-primary" id="{widget_id}_select" disabled>Select Icon</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <script type="text/javascript">
            document.addEventListener('DOMContentLoaded', function() {{
                if (typeof IconPicker !== 'undefined') {{
                    new IconPicker('{widget_id}', {json.dumps(config)});
                }} else {{
                    // Fallback for basic functionality
                    console.warn('IconPicker JavaScript not loaded, using basic functionality');
                }}
            }});
        </script>
        '''
        
        return mark_safe(picker_html)
    
    def _get_available_icon_sets(self):
        """Get list of available icon sets with metadata."""
        return [
            {
                'id': icon_set[0],
                'prefix': icon_set[1],
                'name': icon_set[2],
                'version': icon_set[3] if len(icon_set) > 3 else 'latest',
            }
            for icon_set in ICON_SETS
        ]
    
    def _render_icon_set_options(self):
        """Render option elements for icon set selector."""
        options = []
        for icon_set in ICON_SETS:
            selected = 'selected' if icon_set[0] == self.icon_set else ''
            options.append(f'<option value="{icon_set[0]}" {selected}>{icon_set[2]}</option>')
        return ''.join(options)
    
    def _render_preview(self, value):
        """Render icon preview with backward compatibility."""
        if not value:
            return ''
        
        # Use the field methods for consistent rendering
        try:
            from .fields import IconField
            field = IconField()
            return field.get_display_html(value, css_class="icon-preview")
        except ImportError:
            # Fallback for basic preview
            return f'<span class="icon-preview">{value}</span>'
    
    def _safe_reverse(self, url_name, fallback):
        """Safely reverse URL or return fallback."""
        try:
            return reverse(url_name)
        except:
            return fallback
    
    @property
    def media(self):
        """Return media files needed for the widget."""
        return forms.Media(
            css={
                'all': [
                    static('django_icon_picker/css/icon_picker.css'),
                ]
            },
            js=[
                static('django_icon_picker/js/icon_picker.js'),
            ]
        )


# Backward compatibility - maintain the original class name and interface
class IconPicker(IconPickerWidget):
    """
    Backward compatibility alias for the original widget name.
    Maintains the original template and behavior.
    """
    
    template_name = "django_icon_picker/icon_picker.html"
    
    def get_settings_attr(self, context, key, attr):
        """Original method for settings access."""
        try:
            from django.conf import settings
            context[key] = getattr(settings, attr)
        except:
            pass

    def get_context(self, name, value, attrs):
        """Original get_context method for template compatibility."""
        context = super().get_context(name, value, attrs)
        self.get_settings_attr(context, "save_path", "ICON_PICKER_PATH")
        self.get_settings_attr(context, "default_color", "ICON_PICKER_COLOR")
        context.update(
            {
                "object_id": self.get_object_id(value),
            }
        )
        return context

    def get_object_id(self, value):
        """Original object ID generation."""
        if value:
            return value.split("/")[-1].split(".")[0].replace("icon-", "")
        import uuid
        return str(uuid.uuid4())

    class Media:
        """Original media configuration."""
        css = {
            "all": (
                "https://cdn.jsdelivr.net/gh/mdbasit/Coloris@latest/dist/coloris.min.css",
                "django_icon_picker/css/icon_picker.css",
            )
        }
        js = (
            "https://cdn.jsdelivr.net/gh/mdbasit/Coloris@latest/dist/coloris.min.js",
            "django_icon_picker/js/icon_picker.js",
        )


class SimpleIconPickerWidget(forms.Select):
    """Simplified icon picker widget for basic use cases."""
    
    def __init__(self, icon_set='fontawesome5solid', attrs=None):
        self.icon_set = icon_set
        choices = self._get_icon_choices()
        super().__init__(choices=choices, attrs=attrs)
    
    def _get_icon_choices(self):
        """Get simplified icon choices for the select widget."""
        return [
            ('', '-- Select an icon --'),
            ('😀', 'Happy'),
            ('😎', 'Cool'),
            ('❤️', 'Heart'),
            ('⭐', 'Star'),
            ('🏠', 'Home'),
            ('👤', 'User'),
            ('🔍', 'Search'),
            ('⚙️', 'Settings'),
            ('📧', 'Email'),
            ('📞', 'Phone'),
        ]


class EmojiPickerWidget(IconPickerWidget):
    """
    Specialized widget for emoji selection (backward compatibility).
    """
    
    def __init__(self, attrs=None):
        super().__init__(
            allow_svg=False,
            allow_custom=False,
            allow_emoji=True,
            icon_set=None,
            attrs=attrs
        )
