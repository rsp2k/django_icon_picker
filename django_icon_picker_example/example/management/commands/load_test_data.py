"""
Management command to load test fixtures and verify icon picker data.
"""
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import transaction
from example.models import ExampleModel


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

    def verify_data(self):
        """Verify the loaded data."""
        self.stdout.write('🔍 Verifying loaded data...')
        
        total_count = ExampleModel.objects.count()
        
        if total_count == 0:
            self.stdout.write(
                self.style.WARNING('   ⚠️  No data found in database')
            )
            return
            
        # Group by icon set
        icon_sets = {}
        for obj in ExampleModel.objects.all():
            if ':' in obj.icon:
                icon_set = obj.icon.split(':')[0]
                if icon_set not in icon_sets:
                    icon_sets[icon_set] = []
                icon_sets[icon_set].append(obj)
            else:
                if 'other' not in icon_sets:
                    icon_sets['other'] = []
                icon_sets['other'].append(obj)
        
        self.stdout.write(f'   📊 Total records: {total_count}')
        
        for icon_set, objects in icon_sets.items():
            self.stdout.write(f'   📁 {icon_set}: {len(objects)} icons')
            
        # Check for any empty icons or names
        empty_icons = ExampleModel.objects.filter(icon='').count()
        empty_names = ExampleModel.objects.filter(name='').count()
        
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
        self.stdout.write('   • comprehensive_test_data.json - 40 diverse icons (recommended)')
        self.stdout.write('   • basic_icons.json - 15 Material Symbols icons')
        self.stdout.write('   • brand_icons.json - 10 Font Awesome brand icons')
        self.stdout.write('   • heroicons.json - 10 Heroicons')
        
        self.stdout.write('\n🚀 Usage Examples:')
        self.stdout.write('   python manage.py load_test_data')
        self.stdout.write('   python manage.py load_test_data --fixture=basic_icons')
        self.stdout.write('   python manage.py load_test_data --clear')
        self.stdout.write('   python manage.py load_test_data --verify-only')
        
        self.stdout.write('\n🎯 Next Steps:')
        self.stdout.write('   1. Visit /admin/ to see the icon picker in action')
        self.stdout.write('   2. Navigate to /admin/example/examplemodel/ to see the icon list')
        self.stdout.write('   3. Try adding a new model with /admin/example/examplemodel/add/')
        
        self.stdout.write(
            self.style.SUCCESS('\n🎉 Ready for screenshot testing!')
        )
