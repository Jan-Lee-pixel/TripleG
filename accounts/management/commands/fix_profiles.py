from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Profile
from django.db import transaction

class Command(BaseCommand):
    help = 'Fix profile data inconsistencies and ensure each user has their own profile'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Starting profile fix...'))
        
        with transaction.atomic():
            # 1. Delete orphaned profiles (profiles without users)
            orphaned_profiles = Profile.objects.filter(user__isnull=True)
            orphaned_count = orphaned_profiles.count()
            orphaned_profiles.delete()
            self.stdout.write(f'Deleted {orphaned_count} orphaned profiles')
            
            # 2. Delete duplicate profiles (multiple profiles for same user)
            users_with_multiple_profiles = []
            for user in User.objects.all():
                profiles = Profile.objects.filter(user=user)
                if profiles.count() > 1:
                    users_with_multiple_profiles.append(user)
                    # Keep the first profile, delete the rest
                    profiles_to_delete = profiles[1:]
                    for profile in profiles_to_delete:
                        profile.delete()
                    self.stdout.write(f'Fixed duplicate profiles for user: {user.username}')
            
            # 3. Create missing profiles for users without profiles
            users_without_profiles = User.objects.filter(profile__isnull=True)
            created_count = 0
            for user in users_without_profiles:
                Profile.objects.create(user=user, role='customer')
                created_count += 1
                self.stdout.write(f'Created profile for user: {user.username}')
            
            # 4. Verify all profiles are correctly linked
            total_users = User.objects.count()
            total_profiles = Profile.objects.count()
            
            self.stdout.write(self.style.SUCCESS(
                f'Profile fix complete!\n'
                f'Total users: {total_users}\n'
                f'Total profiles: {total_profiles}\n'
                f'Created {created_count} new profiles\n'
                f'Fixed {len(users_with_multiple_profiles)} users with duplicate profiles\n'
                f'Deleted {orphaned_count} orphaned profiles'
            ))
            
            if total_users != total_profiles:
                self.stdout.write(self.style.ERROR(
                    'WARNING: User count does not match profile count!'
                ))
            else:
                self.stdout.write(self.style.SUCCESS(
                    'SUCCESS: Each user now has exactly one profile!'
                ))
