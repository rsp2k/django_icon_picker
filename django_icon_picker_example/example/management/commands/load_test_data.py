"""
Management command to load test fixtures and verify icon picker data.
"""
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import transaction
from example.models import ExampleModel
import re


class Command(BaseCommand):
    help = 'Load test fixtures for the Django Icon Picker example and verify data'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--fixture',
            type=str,
            default='comprehensive_test_data',
            help='Which fixture to load (default: comprehensive_test_data)',
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before loading fixtures',
        )
        parser.add_argument(
            '--verify-only',
            action='store_true',
            help='Only verify existing data, do not load fixtures',
        )

    def handle(self, *args, **options):
        fixture_name = options['fixture']
        clear_data = options['clear']
        verify_only = options['verify_only']
        
        self.stdout.write(
            self.style.SUCCESS('🎨 Django Icon Picker Test Data Manager')
        )
        self.stdout.write('=' * 50)
        
        if verify_only:
            self.verify_data()
            return
            
        if clear_data:
            self.clear_existing_data()
            
        self.load_fixtures(fixture_name)
        self.verify_data()
        self.display_summary()

    def clear_existing_data(self):
        """Clear existing ExampleModel data."""
        self.stdout.write('🗑️  Clearing existing data...')
        
        with transaction.atomic():
            count = ExampleModel.objects.count()
            ExampleModel.objects.all().delete()
            
        self.stdout.write(
            self.style.WARNING(f'   Deleted {count} existing records')
        )

    def load_fixtures(self, fixture_name):
        """Load the specified fixture."""
        fixture_file = f'example/fixtures/{fixture_name}.json'
        
        self.stdout.write(f'📦 Loading fixture: {fixture_file}')
        
        try:
            call_command('loaddata', fixture_file, verbosity=0)
            self.stdout.write(
                self.style.SUCCESS('   ✅ Fixtures loaded successfully')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'   ❌ Failed to load fixtures: {e}')
            )
            raise

    def is_emoji(self, text):
        """Check if a string contains emoji characters."""
        # Basic emoji detection pattern
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map
            "\U0001F1E0-\U0001F1FF"  # flags (iOS)
            "\U00002702-\U000027B0"  # misc symbols
            "\U000024C2-\U0001F251"  # enclosed characters
            "]+", flags=re.UNICODE
        )
        return bool(emoji_pattern.search(text))

    def categorize_icons(self):
        """Categorize icons into emojis vs icon sets."""
        all_objects = ExampleModel.objects.all()
        
        categories = {
            'emojis': [],
            'material-symbols': [],
            'fa-brands': [],
            'heroicons': [],
            'mdi': [],
            'other': []
        }
        
        for obj in all_objects:
            if self.is_emoji(obj.icon):
                categories['emojis'].append(obj)
            elif ':' in obj.icon:
                icon_set = obj.icon.split(':')[0]
                if icon_set in categories:
                    categories[icon_set].append(obj)
                else:
                    categories['other'].append(obj)
            else:
                categories['other'].append(obj)
                
        return categories

    def verify_data(self):
        """Verify the loaded data with enhanced emoji support."""
        self.stdout.write('🔍 Verifying loaded data...')
        
        total_count = ExampleModel.objects.count()
        
        if total_count == 0:
            self.stdout.write(
                self.style.WARNING('   ⚠️  No data found in database')
            )
            return
            
        # Categorize by type
        categories = self.categorize_icons()
        
        self.stdout.write(f'   📊 Total records: {total_count}')
        
        # Report on each category
        for category, objects in categories.items():
            if objects:
                if category == 'emojis':
                    self.stdout.write(f'   😀 {category}: {len(objects)} emojis')
                    # Show first few emojis as examples
                    sample_emojis = [obj.icon for obj in objects[:5]]
                    self.stdout.write(f'      Examples: {" ".join(sample_emojis)}')
                else:
                    self.stdout.write(f'   📁 {category}: {len(objects)} icons')
        
        # Check for any empty icons or names
        empty_icons = ExampleModel.objects.filter(icon='').count()
        empty_names = ExampleModel.objects.filter(name='').count()
        
        # Check for emoji vs icon mix
        emoji_count = len(categories['emojis'])
        icon_count = total_count - emoji_count
        
        if emoji_count > 0 and icon_count > 0:
            self.stdout.write(
                self.style.SUCCESS(f'   🎯 Mixed content: {emoji_count} emojis + {icon_count} icons')
            )
        elif emoji_count > 0:
            self.stdout.write(
                self.style.SUCCESS(f'   😀 Emoji-only dataset: {emoji_count} emojis')
            )
        elif icon_count > 0:
            self.stdout.write(
                self.style.SUCCESS(f'   🎨 Icon-only dataset: {icon_count} icons')
            )
        
        if empty_icons > 0:
            self.stdout.write(
                self.style.WARNING(f'   ⚠️  {empty_icons} records with empty icons')
            )
            
        if empty_names > 0:
            self.stdout.write(
                self.style.WARNING(f'   ⚠️  {empty_names} records with empty names')
            )
            
        if empty_icons == 0 and empty_names == 0:
            self.stdout.write(
                self.style.SUCCESS('   ✅ All records have valid data')
            )

    def display_summary(self):
        """Display a summary of available fixtures and usage."""
        self.stdout.write('\n📋 Available Fixtures:')
        self.stdout.write('   🎯 comprehensive_test_data.json - 60 mixed icons + emojis (recommended)')
        self.stdout.write('   😀 emoji_categories.json - 50 emojis across all categories')
        self.stdout.write('   🎉 emoji_showcase.json - 20 popular emojis')
        self.stdout.write('   🔄 mixed_icons_emojis.json - 20 icon vs emoji comparisons')
        self.stdout.write('   📱 basic_icons.json - 15 Material Symbols icons')
        self.stdout.write('   🔗 brand_icons.json - 10 Font Awesome brand icons')
        self.stdout.write('   🎨 heroicons.json - 10 Heroicons')
        
        self.stdout.write('\n🚀 Usage Examples:')
        self.stdout.write('   python manage.py load_test_data')
        self.stdout.write('   python manage.py load_test_data --fixture=emoji_categories')
        self.stdout.write('   python manage.py load_test_data --fixture=mixed_icons_emojis')
        self.stdout.write('   python manage.py load_test_data --clear')
        self.stdout.write('   python manage.py load_test_data --verify-only')
        
        self.stdout.write('\n🎯 Next Steps:')
        self.stdout.write('   1. Visit /admin/ to see both icons and emojis in action')
        self.stdout.write('   2. Navigate to /admin/example/examplemodel/ to see the mixed list')
        self.stdout.write('   3. Try /admin/example/examplemodel/add/ for emoji picker demo')
        self.stdout.write('   4. Toggle between icon and emoji modes in the picker')
        
        self.stdout.write('\n💡 Pro Tips:')
        self.stdout.write('   • Emojis render instantly on all devices')
        self.stdout.write('   • Icons can be customized with colors')
        self.stdout.write('   • Use mixed fixtures to showcase dual functionality')
        self.stdout.write('   • Emoji categories cover all use cases mentioned in README')
        
        self.stdout.write(
            self.style.SUCCESS('\n🎉 Ready for emoji + icon screenshot testing!')
        )
