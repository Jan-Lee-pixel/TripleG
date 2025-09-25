from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.utils import timezone
from accounts.models import AdminProfile
from accounts.utils import send_admin_approval_email, send_admin_denial_email, send_admin_suspension_email


class Command(BaseCommand):
    help = 'Manage admin account approvals (approve, deny, suspend, list)'

    def add_arguments(self, parser):
        parser.add_argument(
            'action',
            choices=['approve', 'deny', 'suspend', 'list'],
            help='Action to perform'
        )
        parser.add_argument(
            '--email',
            type=str,
            help='Email of the admin to manage'
        )
        parser.add_argument(
            '--all-pending',
            action='store_true',
            help='Apply action to all pending admins'
        )
        parser.add_argument(
            '--role',
            choices=['admin', 'manager', 'staff', 'site_manager'],
            help='Filter by admin role'
        )
        parser.add_argument(
            '--send-email',
            action='store_true',
            default=True,
            help='Send notification email (default: True)'
        )
        parser.add_argument(
            '--no-email',
            action='store_true',
            help='Do not send notification email'
        )

    def handle(self, *args, **options):
        action = options['action']
        email = options['email']
        all_pending = options['all_pending']
        role_filter = options['role']
        send_email = options['send_email'] and not options['no_email']

        if action == 'list':
            self.list_admins(role_filter)
            return

        if not email and not all_pending:
            raise CommandError('You must specify either --email or --all-pending')

        if email and all_pending:
            raise CommandError('You cannot specify both --email and --all-pending')

        if email:
            # Handle single admin
            try:
                user = User.objects.get(email=email)
                if not hasattr(user, 'adminprofile'):
                    raise CommandError(f'User {email} does not have an admin profile')
                
                admin_profile = user.adminprofile
                self.perform_action(action, admin_profile, send_email)
                
            except User.DoesNotExist:
                raise CommandError(f'User with email {email} does not exist')

        elif all_pending:
            # Handle all pending admins
            queryset = AdminProfile.objects.filter(approval_status='pending')
            
            if role_filter:
                queryset = queryset.filter(admin_role=role_filter)
            
            if not queryset.exists():
                self.stdout.write(
                    self.style.WARNING('No pending admin profiles found')
                )
                return
            
            count = 0
            email_count = 0
            
            for admin_profile in queryset:
                success = self.perform_action(action, admin_profile, send_email)
                count += 1
                if success and send_email:
                    email_count += 1
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully {action}ed {count} admin(s). '
                    f'{email_count} notification email(s) sent.'
                )
            )

    def perform_action(self, action, admin_profile, send_email=True):
        """Perform the specified action on an admin profile"""
        user = admin_profile.user
        
        if action == 'approve':
            admin_profile.approval_status = 'approved'
            admin_profile.approved_at = timezone.now()
            # Note: approved_by would need to be set to a superuser in a real scenario
            admin_profile.save()
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Approved {admin_profile.get_admin_role_display()} account for {user.email}'
                )
            )
            
            if send_email:
                if send_admin_approval_email(admin_profile, None):
                    self.stdout.write(f'  ✓ Approval email sent to {user.email}')
                    return True
                else:
                    self.stdout.write(
                        self.style.ERROR(f'  ✗ Failed to send approval email to {user.email}')
                    )
                    return False
            
        elif action == 'deny':
            admin_profile.approval_status = 'denied'
            admin_profile.save()
            
            self.stdout.write(
                self.style.WARNING(
                    f'Denied {admin_profile.get_admin_role_display()} account for {user.email}'
                )
            )
            
            if send_email:
                if send_admin_denial_email(admin_profile):
                    self.stdout.write(f'  ✓ Denial email sent to {user.email}')
                    return True
                else:
                    self.stdout.write(
                        self.style.ERROR(f'  ✗ Failed to send denial email to {user.email}')
                    )
                    return False
            
        elif action == 'suspend':
            admin_profile.approval_status = 'suspended'
            admin_profile.save()
            
            self.stdout.write(
                self.style.ERROR(
                    f'Suspended {admin_profile.get_admin_role_display()} account for {user.email}'
                )
            )
            
            if send_email:
                if send_admin_suspension_email(admin_profile):
                    self.stdout.write(f'  ✓ Suspension email sent to {user.email}')
                    return True
                else:
                    self.stdout.write(
                        self.style.ERROR(f'  ✗ Failed to send suspension email to {user.email}')
                    )
                    return False
        
        return True

    def list_admins(self, role_filter=None):
        """List admin profiles with their status"""
        queryset = AdminProfile.objects.all().order_by('approval_status', 'created_at')
        
        if role_filter:
            queryset = queryset.filter(admin_role=role_filter)
        
        if not queryset.exists():
            self.stdout.write(self.style.WARNING('No admin profiles found'))
            return
        
        self.stdout.write(self.style.SUCCESS('\nAdmin Profiles:'))
        self.stdout.write('-' * 80)
        
        status_colors = {
            'pending': self.style.WARNING,
            'approved': self.style.SUCCESS,
            'denied': self.style.ERROR,
            'suspended': self.style.ERROR,
        }
        
        for admin_profile in queryset:
            user = admin_profile.user
            status_style = status_colors.get(admin_profile.approval_status, self.style.NOTICE)
            
            status_display = status_style(admin_profile.approval_status.upper())
            
            self.stdout.write(
                f'{user.email:<30} | '
                f'{admin_profile.get_admin_role_display():<15} | '
                f'{status_display:<10} | '
                f'{admin_profile.created_at.strftime("%Y-%m-%d %H:%M")}'
            )
        
        # Summary
        self.stdout.write('-' * 80)
        status_counts = {}
        for status in ['pending', 'approved', 'denied', 'suspended']:
            count = queryset.filter(approval_status=status).count()
            if count > 0:
                status_counts[status] = count
        
        summary = ' | '.join([f'{status.title()}: {count}' for status, count in status_counts.items()])
        self.stdout.write(f'Summary: {summary}')
