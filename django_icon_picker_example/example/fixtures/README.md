# Test Fixtures for Django Icon Picker Example

This directory contains test fixtures to demonstrate both the **icon** and **emoji** functionality of the Django Icon Picker with various icon sets and emoji categories.

## Fixture Files

### `comprehensive_test_data.json`
**🎯 Recommended for screenshots and comprehensive testing**

Contains **60 example records** showcasing both icons and emojis:

- **Icons (40 entries)**: Material Symbols, Font Awesome, Heroicons, Material Design Icons
- **Emojis (20 entries)**: Popular emojis from multiple categories demonstrating emoji picker functionality

### Emoji-Specific Fixtures

**`emoji_categories.json`** - **50 emojis** covering all 8 categories:
- 😀 **Smileys & People**: Happy, sad, thinking, party faces and hand gestures  
- ❤️ **Hearts & Love**: Various colored hearts and love symbols
- 🎉 **Activities**: Party, celebrations, sports, and entertainment
- ⭐ **Symbols**: Stars, checkmarks, warnings, and common symbols  
- 📱 **Objects**: Technology, tools, communication devices
- 🌈 **Nature**: Weather, plants, celestial objects
- 🍕 **Food & Drink**: Popular foods, beverages, and treats
- 🚀 **Transport**: Vehicles, travel, and movement

**`emoji_showcase.json`** - **20 popular emojis** for quick testing

**`mixed_icons_emojis.json`** - **20 side-by-side comparisons** showing icon vs emoji styles:
- Home: `material-symbols:home` vs 🏠
- Heart: `heroicons:heart` vs ❤️  
- Fire: `heroicons:fire` vs 🔥
- Star: `material-symbols:star` vs ⭐
- And more...

### Icon-Only Fixtures

**`basic_icons.json`** - 15 Material Symbols icons for common UI elements  
**`brand_icons.json`** - 10 Font Awesome brand icons for social platforms  
**`heroicons.json`** - 10 Heroicons for modern outline-style icons

## Loading Fixtures

### Load comprehensive test data (recommended):
```bash
python manage.py loaddata comprehensive_test_data.json
```

### Load emoji-specific fixtures:
```bash
# All emoji categories (50 emojis)
python manage.py loaddata emoji_categories.json

# Popular emoji showcase (20 emojis)  
python manage.py loaddata emoji_showcase.json

# Side-by-side icon vs emoji comparison (20 pairs)
python manage.py loaddata mixed_icons_emojis.json
```

### Load specific icon sets:
```bash
# Material Symbols icons
python manage.py loaddata basic_icons.json

# Social media brand icons  
python manage.py loaddata brand_icons.json

# Modern outline icons
python manage.py loaddata heroicons.json
```

### Load all fixtures for maximum variety:
```bash
python manage.py loaddata comprehensive_test_data.json emoji_categories.json mixed_icons_emojis.json
```

## Using the Management Command

The custom `load_test_data` management command supports all fixture types:

```bash
# Load comprehensive data (icons + emojis)
python manage.py load_test_data

# Load emoji-focused data
python manage.py load_test_data --fixture=emoji_categories

# Load mixed comparison data
python manage.py load_test_data --fixture=mixed_icons_emojis

# Clear and reload
python manage.py load_test_data --clear --fixture=emoji_showcase

# Verify existing data
python manage.py load_test_data --verify-only
```

## Emoji Categories Demonstrated

### 😀 Smileys & People (7 emojis)
`😀` `😃` `😊` `🥳` `🤔` `😢` `👋` `👍` `✋`

### ❤️ Hearts & Love (6 emojis)  
`❤️` `💙` `💚` `💜` `🧡` `💛`

### 🎉 Activities (5 emojis)
`🎉` `🎊` `🏆` `🎯` `⚽` `🎵`

### ⭐ Symbols (5 emojis)
`⭐` `🌟` `✨` `🔥` `✅` `❌` `⚠️` `ℹ️`

### 📱 Objects (5 emojis)
`📱` `💻` `⌚` `📧` `🔧`

### 🌈 Nature (5 emojis)  
`🌈` `☀️` `🌙` `🌳` `🌸`

### 🍕 Food & Drink (5 emojis)
`🍕` `🍔` `☕` `🍰` `🥤`

### 🚀 Transport (5 emojis)
`🚀` `🚗` `✈️` `🚲` `🏠`

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

## Screenshot Testing Benefits

The emoji fixtures provide excellent visual variety for screenshot testing:

1. **🎨 Visual Diversity**: Mix of colorful emojis and scalable vector icons
2. **📊 Comparison Views**: Side-by-side icon vs emoji styles  
3. **🌍 Universal Appeal**: Emojis work across all platforms and languages
4. **🎯 Category Coverage**: Demonstrates full emoji picker functionality
5. **📱 Mobile Ready**: Native emoji rendering on all devices

## Using in Screenshots

The fixtures create compelling admin screenshots that show:

- **📋 Rich List Views**: Icons and emojis displayed together in admin lists
- **🔄 Dual Functionality**: Both icon picker and emoji picker working
- **🎨 Visual Appeal**: Colorful emojis mixed with professional vector icons
- **🌟 Real-world Usage**: Realistic names and icon/emoji combinations
- **📐 Responsive Display**: How emojis render across different screen sizes

## Test Data Structure

Each fixture entry uses this structure:
```json
{
  "model": "example.examplemodel",
  "pk": 1,
  "fields": {
    "name": "Descriptive Name",
    "icon": "😀"  // or "icon-set:icon-name"
  }
}
```

**Emojis** are stored directly as Unicode characters: `😀`, `❤️`, `🎉`  
**Icons** use the format: `icon-set:icon-name` (e.g., `material-symbols:star`)

## Adding New Test Data

### For Emojis:
1. Copy the emoji directly: `😀`, `🚀`, `❤️`
2. Use descriptive names that include the emoji: `"😀 Happy Face"`
3. Ensure unique primary keys (pk values)

### For Icons:
1. Choose from [Iconify](https://iconify.design/)
2. Use format: `icon-set:icon-name`
3. Match with similar emoji for comparison fixtures

### Example:
```json
{
  "model": "example.examplemodel", 
  "pk": 61,
  "fields": {
    "name": "🎈 Balloon Party",
    "icon": "🎈"
  }
}
```

## Performance Notes

- **Emojis**: Render instantly (native Unicode support)
- **Icons**: May require API calls for SVG generation (depending on configuration)
- **Mixed fixtures**: Demonstrate both rendering methods in same interface

The emoji fixtures showcase the dual functionality that makes Django Icon Picker unique—supporting both professional vector icons and expressive emojis in the same field!
