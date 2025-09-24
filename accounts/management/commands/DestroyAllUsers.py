from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.db import transaction
from django.conf import settings
from accounts.models import AdminProfile, Profile, OneTimePassword
import os

class Command(BaseCommand):
    help = 'DEVELOPMENT ONLY: Delete all users except superadmins'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm-destroy',
            action='store_true',
            help='Required flag to confirm you want to destroy all non-superadmin users'
        )
        parser.add_argument(
            '--i-understand-this-is-irreversible',
            action='store_true',
            help='Required flag to confirm you understand this action is irreversible'
        )
        parser.add_argument(
            '--development-only',
            action='store_true',
            help='Required flag to confirm this is for development use only'
        )

    def handle(self, *args, **options):
        # Safety check: Only allow in DEBUG mode
        if not settings.DEBUG:
            raise CommandError(
                '🚨 SECURITY BLOCK: This command can only be run in DEBUG mode (development).\n'
                'Set DEBUG=True in settings.py to use this command.'
            )
        
        # Require all confirmation flags
        required_flags = [
            'confirm_destroy',
            'i_understand_this_is_irreversible', 
            'development_only'
        ]
        
        missing_flags = [flag for flag in required_flags if not options.get(flag)]
        if missing_flags:
            self.stdout.write(
                self.style.ERROR(
                    '🚨 MISSING REQUIRED FLAGS:\n'
                    'This is a destructive operation. You must provide ALL of these flags:\n'
                    '  --confirm-destroy\n'
                    '  --i-understand-this-is-irreversible\n'
                    '  --development-only\n\n'
                    'Example usage:\n'
                    'python manage.py DestroyAllUsers --confirm-destroy --i-understand-this-is-irreversible --development-only'
                )
            )
            return

        # Additional safety check for production-like environments
        if 'RENDER' in os.environ or 'HEROKU' in os.environ or 'AWS' in os.environ:
            raise CommandError(
                '🚨 PRODUCTION ENVIRONMENT DETECTED: This command is blocked on production platforms.'
            )

        self.stdout.write(
            self.style.WARNING(
                '🚨 DESTRUCTIVE OPERATION WARNING 🚨\n'
                '=' * 50 + '\n'
                'This will DELETE ALL USERS except superadmins!\n'
                'This includes:\n'
                '  • All admin users (admin, manager, supervisor, staff)\n'
                '  • All client/public users\n'
                '  • All associated profiles and data\n'
                '  • All OTP records\n\n'
                'SUPERADMINS WILL BE PRESERVED\n'
                '=' * 50
            )
        )

        # Show current user counts
        self.show_current_state()
        
        # Final confirmation
        confirm = input('\nType "DESTROY ALL USERS" to proceed (case sensitive): ')
        if confirm != "DESTROY ALL USERS":
            self.stdout.write(self.style.ERROR('❌ Operation cancelled. Confirmation text did not match.'))
            return

        # Execute the destruction
        self.execute_destruction()

    def show_current_state(self):
        """Display current user counts before destruction"""
        superadmin_count = User.objects.filter(is_superuser=True).count()
        admin_count = User.objects.filter(is_staff=True, is_superuser=False).count()
        client_count = User.objects.filter(is_staff=False, is_superuser=False).count()
        total_users = User.objects.count()
        
        admin_profiles_count = AdminProfile.objects.count()
        client_profiles_count = Profile.objects.count()
        otp_count = OneTimePassword.objects.count()

        self.stdout.write(
            self.style.WARNING(
                f'\n📊 CURRENT DATABASE STATE:\n'
                f'  👑 Superadmins: {superadmin_count} (WILL BE PRESERVED)\n'
                f'  👨‍💼 Admin Users: {admin_count} (WILL BE DELETED)\n'
                f'  👤 Client Users: {client_count} (WILL BE DELETED)\n'
                f'  📋 Total Users: {total_users}\n'
                f'  🏢 Admin Profiles: {admin_profiles_count} (WILL BE DELETED)\n'
                f'  👥 Client Profiles: {client_profiles_count} (WILL BE DELETED)\n'
                f'  🔐 OTP Records: {otp_count} (WILL BE DELETED)\n'
                f'\n  🛡️  Users to be preserved: {superadmin_count}\n'
                f'  💥 Users to be destroyed: {admin_count + client_count}\n'
            )
        )

    @transaction.atomic
    def execute_destruction(self):
        """Execute the user destruction with transaction safety"""
        self.stdout.write(self.style.WARNING('\n🔥 BEGINNING DESTRUCTION SEQUENCE...'))
        
        try:
            # Get counts before deletion
            initial_counts = {
                'superadmins': User.objects.filter(is_superuser=True).count(),
                'admins': User.objects.filter(is_staff=True, is_superuser=False).count(),
                'clients': User.objects.filter(is_staff=False, is_superuser=False).count(),
                'admin_profiles': AdminProfile.objects.count(),
                'client_profiles': Profile.objects.count(),
                'otps': OneTimePassword.objects.count(),
            }

            # Step 1: Delete OTP records for non-superadmin users
            self.stdout.write('  🗑️  Deleting OTP records...')
            non_superadmin_users = User.objects.filter(is_superuser=False)
            deleted_otps = OneTimePassword.objects.filter(user__in=non_superadmin_users).delete()[0]
            self.stdout.write(f'    ✓ Deleted {deleted_otps} OTP records')

            # Step 2: Delete AdminProfiles (this will cascade to related data)
            self.stdout.write('  🗑️  Deleting Admin Profiles...')
            deleted_admin_profiles = AdminProfile.objects.all().delete()[0]
            self.stdout.write(f'    ✓ Deleted {deleted_admin_profiles} admin profiles')

            # Step 3: Delete Client Profiles (this will cascade to related data)
            self.stdout.write('  🗑️  Deleting Client Profiles...')
            deleted_client_profiles = Profile.objects.all().delete()[0]
            self.stdout.write(f'    ✓ Deleted {deleted_client_profiles} client profiles')

            # Step 4: Delete non-superadmin users
            self.stdout.write('  🗑️  Deleting non-superadmin users...')
            deleted_users = User.objects.filter(is_superuser=False).delete()[0]
            self.stdout.write(f'    ✓ Deleted {deleted_users} users')

            # Verify final state
            final_counts = {
                'superadmins': User.objects.filter(is_superuser=True).count(),
                'total_users': User.objects.count(),
                'admin_profiles': AdminProfile.objects.count(),
                'client_profiles': Profile.objects.count(),
                'otps': OneTimePassword.objects.count(),
            }

            # Success report
            self.stdout.write(
                self.style.SUCCESS(
                    f'\n🎉 DESTRUCTION COMPLETE!\n'
                    f'=' * 40 + '\n'
                    f'📊 DESTRUCTION SUMMARY:\n'
                    f'  💥 Admin users deleted: {initial_counts["admins"]}\n'
                    f'  💥 Client users deleted: {initial_counts["clients"]}\n'
                    f'  💥 Admin profiles deleted: {initial_counts["admin_profiles"]}\n'
                    f'  💥 Client profiles deleted: {initial_counts["client_profiles"]}\n'
                    f'  💥 OTP records deleted: {deleted_otps}\n'
                    f'  💥 Total users destroyed: {deleted_users}\n\n'
                    f'🛡️  PRESERVED:\n'
                    f'  👑 Superadmins: {final_counts["superadmins"]}\n\n'
                    f'📈 FINAL STATE:\n'
                    f'  📋 Total users remaining: {final_counts["total_users"]}\n'
                    f'  🏢 Admin profiles: {final_counts["admin_profiles"]}\n'
                    f'  👥 Client profiles: {final_counts["client_profiles"]}\n'
                    f'  🔐 OTP records: {final_counts["otps"]}\n\n'
                    f'✅ Database is now clean for development!\n'
                    f'=' * 40
                )
            )

            # Security reminder
            self.stdout.write(
                self.style.WARNING(
                    f'\n⚠️  SECURITY REMINDER:\n'
                    f'  • This command only works in DEBUG mode\n'
                    f'  • Superadmin accounts are preserved\n'
                    f'  • All other user data has been permanently deleted\n'
                    f'  • Use this responsibly in development only!'
                )
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f'❌ DESTRUCTION FAILED: {str(e)}\n'
                    f'Transaction has been rolled back. No data was deleted.'
                )
            )
            raise CommandError(f'Destruction failed: {str(e)}')
