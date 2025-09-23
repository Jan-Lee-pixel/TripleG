from django.core.management.base import BaseCommand
from django.db import connection, transaction

class Command(BaseCommand):
    help = 'Nuclear cleanup - Direct SQL cleanup of all user data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('🚨 NUCLEAR CLEANUP - Direct SQL cleanup!'))
        
        with connection.cursor() as cursor:
            # 1. Show current state
            cursor.execute("SELECT COUNT(*) FROM accounts_onetimepassword;")
            otp_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM accounts_profile;")
            profile_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM auth_user;")
            user_count = cursor.fetchone()[0]
            
            self.stdout.write(f'Before cleanup: Users={user_count}, Profiles={profile_count}, OTPs={otp_count}')
            
            # 2. Delete all data with CASCADE
            cursor.execute("DELETE FROM accounts_onetimepassword;")
            cursor.execute("DELETE FROM accounts_profile;")
            cursor.execute("DELETE FROM auth_user;")
            
            # 3. Reset sequences
            cursor.execute("ALTER SEQUENCE accounts_onetimepassword_id_seq RESTART WITH 1;")
            cursor.execute("ALTER SEQUENCE accounts_profile_id_seq RESTART WITH 1;")
            cursor.execute("ALTER SEQUENCE auth_user_id_seq RESTART WITH 1;")
            
            # 4. Verify cleanup
            cursor.execute("SELECT COUNT(*) FROM accounts_onetimepassword;")
            final_otp_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM accounts_profile;")
            final_profile_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM auth_user;")
            final_user_count = cursor.fetchone()[0]
            
            # 5. Show sequences
            cursor.execute("SELECT last_value FROM auth_user_id_seq;")
            user_seq = cursor.fetchone()[0]
            
            cursor.execute("SELECT last_value FROM accounts_profile_id_seq;")
            profile_seq = cursor.fetchone()[0]
            
            self.stdout.write(self.style.SUCCESS(
                f'🧹 NUCLEAR CLEANUP COMPLETE!\n'
                f'   Users: {user_count} → {final_user_count}\n'
                f'   Profiles: {profile_count} → {final_profile_count}\n'
                f'   OTPs: {otp_count} → {final_otp_count}\n'
                f'   User sequence: {user_seq}\n'
                f'   Profile sequence: {profile_seq}\n'
                f'   Database is now COMPLETELY clean!'
            ))
