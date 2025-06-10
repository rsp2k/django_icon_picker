# Test Fixtures for Django Icon Picker Example

This directory contains test fixtures to demonstrate the Django Icon Picker functionality with various icon sets and use cases.

## Fixture Files

### `comprehensive_test_data.json`
**Recommended for screenshots and testing**

Contains 40 example records showcasing icons from multiple popular icon sets:

- **Material Symbols Icons** (15 entries): Common UI elements like home, settings, notifications
- **Font Awesome Brand Icons** (10 entries): Social media and technology platform icons
- **Heroicons** (10 entries): Clean, modern outline-style icons
- **Material Design Icons** (5 entries): Additional utility and decorative icons

### Individual Fixture Files

For more targeted testing, you can use the individual fixture files:

- `basic_icons.json` - Material Symbols icons for common UI elements
- `brand_icons.json` - Font Awesome brand icons for social platforms
- `heroicons.json` - Heroicons for modern outline-style icons

## Loading Fixtures

### Load all test data (recommended):
```bash
python manage.py loaddata comprehensive_test_data.json
```

### Load specific fixture sets:
```bash
# Load basic UI icons
python manage.py loaddata basic_icons.json

# Load brand/social media icons  
python manage.py loaddata brand_icons.json

# Load heroicons
python manage.py loaddata heroicons.json
```

### Load multiple fixtures:
```bash
python manage.py loaddata basic_icons.json brand_icons.json heroicons.json
```

## Icon Sets Demonstrated

### Material Symbols
- Format: `material-symbols:icon-name`
- Examples: `material-symbols:home`, `material-symbols:settings`
- Style: Filled, rounded Google Material Design icons

### Font Awesome
- Format: `fa-brands:icon-name` (for brand icons)
- Examples: `fa-brands:github`, `fa-brands:twitter`
- Style: Popular social media and technology brand icons

### Heroicons
- Format: `heroicons:icon-name`
- Examples: `heroicons:academic-cap`, `heroicons:camera`
- Style: Beautiful hand-crafted SVG icons by the makers of Tailwind CSS

### Material Design Icons (MDI)
- Format: `mdi:icon-name`
- Examples: `mdi:weather-sunny`, `mdi:heart`
- Style: Community-driven Material Design icon collection

## Using in Screenshots

The comprehensive test data creates a rich dataset that will make admin screenshots more visually appealing and demonstrate:

1. **List View**: Shows multiple icons in the admin list with the `svg_icon` display
2. **Icon Variety**: Demonstrates different icon sets working together
3. **Real-world Usage**: Realistic names and icon combinations
4. **Visual Impact**: Creates an engaging admin interface for demonstrations

## Test Data Structure

Each fixture entry follows this structure:
```json
{
  "model": "example.examplemodel",
  "pk": 1,
  "fields": {
    "name": "Descriptive Name",
    "icon": "icon-set:icon-name"
  }
}
```

The icon field uses the format supported by the Django Icon Picker, which typically corresponds to icon names from services like [Iconify](https://iconify.design/).

## Adding New Test Data

To add new test data:

1. Choose an appropriate icon from [Iconify](https://iconify.design/)
2. Use the format: `icon-set:icon-name`
3. Add a descriptive name that makes sense for the icon
4. Ensure unique primary keys (pk values)

Example:
```json
{
  "model": "example.examplemodel", 
  "pk": 41,
  "fields": {
    "name": "New Feature",
    "icon": "lucide:sparkles"
  }
}
```
