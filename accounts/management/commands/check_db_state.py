from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Profile

class Command(BaseCommand):
    help = 'Check current database state for users and profiles'

    def handle(self, *args, **options):
        users = User.objects.all()
        profiles = Profile.objects.all()
        
        self.stdout.write(f'Total Users: {users.count()}')
        self.stdout.write(f'Total Profiles: {profiles.count()}')
        
        self.stdout.write('\nUser-Profile mapping:')
        for user in users:
            try:
                profile = user.profile
                self.stdout.write(f'  User {user.id} ({user.username}) -> Profile {profile.id} ({profile.role})')
            except Profile.DoesNotExist:
                self.stdout.write(f'  User {user.id} ({user.username}) -> NO PROFILE')
        
        self.stdout.write('\nProfile-User mapping:')
        for profile in profiles:
            if profile.user:
                self.stdout.write(f'  Profile {profile.id} -> User {profile.user.id} ({profile.user.username})')
            else:
                self.stdout.write(f'  Profile {profile.id} -> NO USER (ORPHANED)')
