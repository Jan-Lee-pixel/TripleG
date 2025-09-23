from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Profile

class Command(BaseCommand):
    help = 'Debug user data mixing issues'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Debugging user data...'))
        
        # Show all users and their profiles
        users = User.objects.all().order_by('id')
        
        for user in users:
            self.stdout.write(f'\n=== USER {user.id} ===')
            self.stdout.write(f'Username: {user.username}')
            self.stdout.write(f'Email: {user.email}')
            self.stdout.write(f'First Name: {user.first_name}')
            self.stdout.write(f'Last Name: {user.last_name}')
            self.stdout.write(f'Is Active: {user.is_active}')
            self.stdout.write(f'Date Joined: {user.date_joined}')
            self.stdout.write(f'Last Login: {user.last_login}')
            
            try:
                profile = user.profile
                self.stdout.write(f'Profile ID: {profile.id}')
                self.stdout.write(f'Profile Role: {profile.role}')
                self.stdout.write(f'Profile Phone: {profile.phone}')
                self.stdout.write(f'Profile Architect: {profile.assigned_architect}')
                self.stdout.write(f'Profile Project: {profile.project_name}')
                self.stdout.write(f'Profile Start: {profile.project_start}')
            except Profile.DoesNotExist:
                self.stdout.write('NO PROFILE!')
        
        # Check for any orphaned profiles
        self.stdout.write(f'\n=== ORPHANED PROFILES ===')
        orphaned_profiles = Profile.objects.filter(user__isnull=True)
        if orphaned_profiles.exists():
            for profile in orphaned_profiles:
                self.stdout.write(f'Orphaned Profile ID: {profile.id}')
        else:
            self.stdout.write('No orphaned profiles found.')
            
        # Check for duplicate profiles
        self.stdout.write(f'\n=== DUPLICATE PROFILE CHECK ===')
        for user in users:
            profiles = Profile.objects.filter(user=user)
            if profiles.count() > 1:
                self.stdout.write(f'User {user.username} has {profiles.count()} profiles!')
                for profile in profiles:
                    self.stdout.write(f'  Profile {profile.id}: {profile.phone}, {profile.assigned_architect}')
            elif profiles.count() == 0:
                self.stdout.write(f'User {user.username} has NO profile!')
                
        # Show profiles by ID
        self.stdout.write(f'\n=== ALL PROFILES BY ID ===')
        profiles = Profile.objects.all().order_by('id')
        for profile in profiles:
            user = profile.user
            self.stdout.write(f'Profile {profile.id} -> User {user.id} ({user.username})')
            self.stdout.write(f'  Phone: {profile.phone}')
            self.stdout.write(f'  Architect: {profile.assigned_architect}')
            self.stdout.write(f'  Project: {profile.project_name}')
