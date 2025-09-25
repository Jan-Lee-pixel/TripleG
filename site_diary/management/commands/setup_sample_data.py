from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, timedelta
from site_diary.models import (
    Project, DiaryEntry, LaborEntry, MaterialEntry, 
    EquipmentEntry, DelayEntry, VisitorEntry
)

class Command(BaseCommand):
    help = 'Create sample data for site diary app testing'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating sample data for site diary app...'))
        
        # Create sample users if they don't exist
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(f'Created admin user: {admin_user.username}')
        
        project_manager, created = User.objects.get_or_create(
            username='pm_john',
            defaults={
                'email': 'john@example.com',
                'first_name': 'John',
                'last_name': 'Smith',
                'is_staff': True
            }
        )
        if created:
            project_manager.set_password('pm123')
            project_manager.save()
            self.stdout.write(f'Created project manager: {project_manager.username}')
        
        architect, created = User.objects.get_or_create(
            username='arch_jane',
            defaults={
                'email': 'jane@example.com',
                'first_name': 'Jane',
                'last_name': 'Doe',
                'is_staff': False
            }
        )
        if created:
            architect.set_password('arch123')
            architect.save()
            self.stdout.write(f'Created architect: {architect.username}')
        
        # Create sample projects
        project1, created = Project.objects.get_or_create(
            name='Downtown Office Complex',
            defaults={
                'description': 'Modern 20-story office building with retail space',
                'client_name': 'ABC Corporation',
                'project_manager': project_manager,
                'architect': architect,
                'location': '123 Main Street, Downtown',
                'start_date': date.today() - timedelta(days=30),
                'expected_end_date': date.today() + timedelta(days=365),
                'budget': 5000000.00,
                'status': 'active'
            }
        )
        if created:
            self.stdout.write(f'Created project: {project1.name}')
        
        project2, created = Project.objects.get_or_create(
            name='Residential Complex Phase 1',
            defaults={
                'description': '50-unit residential apartment complex',
                'client_name': 'XYZ Developers',
                'project_manager': project_manager,
                'architect': architect,
                'location': '456 Oak Avenue, Suburbs',
                'start_date': date.today() - timedelta(days=60),
                'expected_end_date': date.today() + timedelta(days=300),
                'budget': 3000000.00,
                'status': 'active'
            }
        )
        if created:
            self.stdout.write(f'Created project: {project2.name}')
        
        # Create sample diary entries
        for i in range(5):
            entry_date = date.today() - timedelta(days=i)
            
            diary_entry, created = DiaryEntry.objects.get_or_create(
                project=project1,
                entry_date=entry_date,
                defaults={
                    'created_by': project_manager,
                    'weather_condition': 'sunny' if i % 2 == 0 else 'cloudy',
                    'temperature_high': 25 + i,
                    'temperature_low': 15 + i,
                    'humidity': 60 + i * 5,
                    'wind_speed': 10.5,
                    'work_description': f'Foundation work continued on day {i+1}. Concrete pouring for sections A-C completed.',
                    'progress_percentage': 15.5 + i * 2,
                    'quality_issues': 'Minor concrete surface irregularities noted in section B' if i == 2 else '',
                    'safety_incidents': '',
                    'general_notes': f'Good progress made today. Weather conditions favorable.',
                    'photos_taken': True,
                    'approved': i < 3  # Approve first 3 entries
                }
            )
            
            if created:
                self.stdout.write(f'Created diary entry for {entry_date}')
                
                # Add labor entries
                LaborEntry.objects.create(
                    diary_entry=diary_entry,
                    labor_type='skilled',
                    trade_description='Concrete Workers',
                    workers_count=8,
                    hours_worked=8.0,
                    hourly_rate=25.00,
                    overtime_hours=2.0 if i % 3 == 0 else 0,
                    work_area='Foundation Section A-C',
                    notes='Experienced crew, good productivity'
                )
                
                LaborEntry.objects.create(
                    diary_entry=diary_entry,
                    labor_type='unskilled',
                    trade_description='General Laborers',
                    workers_count=4,
                    hours_worked=8.0,
                    hourly_rate=18.00,
                    work_area='Site cleanup and material handling'
                )
                
                # Add material entries
                MaterialEntry.objects.create(
                    diary_entry=diary_entry,
                    material_name='Ready Mix Concrete',
                    quantity_delivered=25.0,
                    quantity_used=22.0,
                    unit='m3',
                    unit_cost=120.00,
                    supplier='City Concrete Co.',
                    delivery_time='08:30',
                    quality_check=True,
                    storage_location='On-site pour',
                    notes='Grade 30 concrete as specified'
                )
                
                MaterialEntry.objects.create(
                    diary_entry=diary_entry,
                    material_name='Rebar Steel',
                    quantity_delivered=500.0,
                    quantity_used=450.0,
                    unit='kg',
                    unit_cost=1.20,
                    supplier='Steel Supply Inc.',
                    storage_location='Material yard section B'
                )
                
                # Add equipment entries
                EquipmentEntry.objects.create(
                    diary_entry=diary_entry,
                    equipment_name='CAT 320D Excavator',
                    equipment_type='Excavator',
                    operator_name='Mike Johnson',
                    hours_operated=7.5,
                    fuel_consumption=45.0,
                    status='operational',
                    rental_cost_per_hour=85.00,
                    work_area='Foundation excavation'
                )
                
                # Add delay entry occasionally
                if i == 1:
                    DelayEntry.objects.create(
                        diary_entry=diary_entry,
                        category='weather',
                        description='Heavy rain in the morning delayed concrete pour by 2 hours',
                        start_time='09:00',
                        end_time='11:00',
                        duration_hours=2.0,
                        impact_level='medium',
                        affected_activities='Concrete pouring, finishing work',
                        mitigation_actions='Covered work area, rescheduled pour to afternoon',
                        responsible_party='Weather conditions',
                        cost_impact=500.00
                    )
                
                # Add visitor entry occasionally
                if i == 0:
                    VisitorEntry.objects.create(
                        diary_entry=diary_entry,
                        visitor_name='Robert Wilson',
                        company='City Building Inspector',
                        visitor_type='inspector',
                        arrival_time='10:00',
                        departure_time='11:30',
                        purpose_of_visit='Foundation inspection and approval',
                        areas_visited='Foundation sections A, B, C',
                        accompanied_by='John Smith (PM)',
                        notes='Inspection passed, minor recommendations noted'
                    )
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created sample data for site diary app!')
        )
        self.stdout.write('Sample users created:')
        self.stdout.write(f'  - Admin: admin/admin123')
        self.stdout.write(f'  - Project Manager: pm_john/pm123')
        self.stdout.write(f'  - Architect: arch_jane/arch123')
