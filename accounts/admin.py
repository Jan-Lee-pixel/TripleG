from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.urls import reverse
from .models import Profile, AdminProfile, OneTimePassword


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'phone', 'assigned_architect')
    list_filter = ('role',)
    search_fields = ('user__username', 'user__email', 'phone')


@admin.register(AdminProfile)
class AdminProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'admin_role', 'approval_status', 'department', 
        'employee_id', 'failed_login_attempts', 'created_at'
    )
    list_filter = ('admin_role', 'approval_status', 'department')
    search_fields = ('user__username', 'user__email', 'employee_id', 'department')
    readonly_fields = ('created_at', 'updated_at', 'last_login_ip', 'failed_login_attempts')
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'admin_role', 'department', 'employee_id')
        }),
        ('Approval Status', {
            'fields': ('approval_status', 'approved_by', 'approved_at')
        }),
        ('Contact Information', {
            'fields': ('phone', 'emergency_contact', 'hire_date')
        }),
        ('Security Information', {
            'fields': ('last_login_ip', 'failed_login_attempts', 'account_locked_until'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['approve_admins', 'deny_admins', 'suspend_admins']
    
    def approve_admins(self, request, queryset):
        from django.utils import timezone
        from django.core.mail import send_mail
        from django.conf import settings
        
        approved_count = 0
        email_sent_count = 0
        
        for admin_profile in queryset:
            # Update approval status
            admin_profile.approval_status = 'approved'
            admin_profile.approved_by = request.user
            admin_profile.approved_at = timezone.now()
            admin_profile.save()
            approved_count += 1
            
            # Send approval email
            user = admin_profile.user
            subject = 'Site Manager Account Approved - Triple G BuildHub'
            message = f'''
Hello {user.first_name},

Great news! Your Site Manager account has been approved by our admin team.

You can now log in to your account and start using Triple G BuildHub's site management features:
- Create and manage site diaries
- Collaborate with teams and clients
- Access all construction project management tools

Login URL: http://127.0.0.1:8000/accounts/sitemanager/login/

Your login credentials:
- Email: {user.email}
- Password: [Use the password you created during registration]

Welcome to Triple G BuildHub!

Best regards,
Triple G BuildHub Team
            '''
            
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
                email_sent_count += 1
            except Exception as e:
                print(f"Failed to send approval email to {user.email}: {str(e)}")
        
        self.message_user(request, f'{approved_count} admin(s) approved successfully. {email_sent_count} notification email(s) sent.')
    approve_admins.short_description = "Approve selected admin accounts"
    
    def deny_admins(self, request, queryset):
        from django.core.mail import send_mail
        from django.conf import settings
        
        denied_count = 0
        email_sent_count = 0
        
        for admin_profile in queryset:
            admin_profile.approval_status = 'denied'
            admin_profile.save()
            denied_count += 1
            
            # Send denial email
            user = admin_profile.user
            subject = 'Site Manager Account Application Update - Triple G BuildHub'
            message = f'''
Hello {user.first_name},

Thank you for your interest in becoming a Site Manager with Triple G BuildHub.

After reviewing your application, we are unable to approve your account at this time. This could be due to various reasons such as incomplete information or current capacity limitations.

If you believe this is an error or would like to reapply in the future, please contact our support team.

Thank you for your understanding.

Best regards,
Triple G BuildHub Team
            '''
            
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
                email_sent_count += 1
            except Exception as e:
                print(f"Failed to send denial email to {user.email}: {str(e)}")
        
        self.message_user(request, f'{denied_count} admin(s) denied. {email_sent_count} notification email(s) sent.')
    deny_admins.short_description = "Deny selected admin accounts"
    
    def suspend_admins(self, request, queryset):
        updated = queryset.update(approval_status='suspended')
        self.message_user(request, f'{updated} admin(s) suspended.')
    suspend_admins.short_description = "Suspend selected admin accounts"


@admin.register(OneTimePassword)
class OneTimePasswordAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'created_at', 'is_expired')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at',)
    
    def is_expired(self, obj):
        return obj.is_expired()
    is_expired.boolean = True
    is_expired.short_description = 'Expired'


# Extend the default User admin to show admin profiles
class AdminProfileInline(admin.StackedInline):
    model = AdminProfile
    can_delete = False
    verbose_name_plural = 'Admin Profile'
    readonly_fields = ('created_at', 'updated_at', 'last_login_ip', 'failed_login_attempts')
    fields = ('admin_role', 'approval_status', 'department', 'employee_id', 'phone', 'emergency_contact', 'hire_date')


class CustomUserAdmin(BaseUserAdmin):
    inlines = (AdminProfileInline,)
    
    def get_inline_instances(self, request, obj=None):
        if obj and obj.is_staff:
            return super().get_inline_instances(request, obj)
        return []


# Comment out the custom user admin for now to avoid conflicts
# admin.site.unregister(User)
# admin.site.register(User, CustomUserAdmin)