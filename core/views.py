from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from accounts.models import Profile
from accounts.forms import ProfileUpdateForm
from accounts.decorators import allow_public_access, require_public_role

@allow_public_access
def home(request):
    return render(request, 'core/home.html')

@allow_public_access
def about(request):
    return render(request, 'core/aboutus.html')

@allow_public_access
def contact(request):
    return render(request, 'core/contacts.html')

@allow_public_access
def project(request):
    return render(request, 'core/project.html')

@require_public_role
@login_required
@never_cache
@csrf_protect
@transaction.atomic
def usersettings(request):
    """
    User Settings View - Ensures each user only sees and edits their own data
    Security: Uses request.user for all queries, never accepts user ID from request
    """
    # Debug: Print current user info
    print(f"[DEBUG] USERSETTINGS - Current user: {request.user.username} (ID: {request.user.id})")
    
    # SECURITY: Always use request.user - never trust user input for user identification
    current_user = request.user
    
    # Get or create profile for the CURRENT USER ONLY
    try:
        profile = Profile.objects.select_for_update().get(user=current_user)
        print(f"[DEBUG] USERSETTINGS - Found existing profile for user: {current_user.username}")
    except Profile.DoesNotExist:
        # Create profile if it doesn't exist (signal should handle this, but fallback)
        profile = Profile.objects.create(user=current_user, role='customer')
        print(f"[DEBUG] USERSETTINGS - Created new profile for user: {current_user.username}")
    
    # SECURITY CHECK: Verify profile belongs to current user
    if profile.user != current_user:
        print(f"[SECURITY ERROR] Profile user mismatch! Profile belongs to {profile.user}, current user is {current_user}")
        messages.error(request, 'Security error: Profile access denied.')
        return redirect('core:home')
    
    print(f"[DEBUG] USERSETTINGS - Profile verified for user: {profile.user.username} (Profile ID: {profile.id})")
    print(f"[DEBUG] USERSETTINGS - Profile data: phone={profile.phone}, architect={profile.assigned_architect}, project={profile.project_name}")
    
    if request.method == 'POST':
        # SECURITY: Pass current_user explicitly to form
        form = ProfileUpdateForm(
            request.POST, 
            request.FILES, 
            instance=profile, 
            user=current_user
        )
        
        if form.is_valid():
            # SECURITY: Double-check user ownership before saving
            if profile.user != current_user:
                print(f"[SECURITY ERROR] Attempted to save profile for wrong user!")
                messages.error(request, 'Security error: Unauthorized profile update.')
                return redirect('core:usersettings')
            
            try:
                # Save with explicit user parameter
                with transaction.atomic():
                    updated_profile = form.save(user=current_user)
                    print(f"[DEBUG] USERSETTINGS - Profile updated for user: {updated_profile.user.username}")
                    print(f"[DEBUG] USERSETTINGS - Updated data: {current_user.first_name} {current_user.last_name}, {updated_profile.phone}, {updated_profile.assigned_architect}")
                    
                    # Success message with user's name
                    user_name = current_user.get_full_name() or current_user.username
                    messages.success(request, f'🎉 Profile updated successfully, {user_name}! Your changes have been saved.')
                    
                return redirect('core:usersettings')
                
            except Exception as e:
                print(f"[ERROR] USERSETTINGS - Failed to save profile: {str(e)}")
                messages.error(request, f'Failed to update profile: {str(e)}')
                
        else:
            messages.error(request, 'Please correct the errors below.')
            print(f"[DEBUG] USERSETTINGS - Form errors: {form.errors}")
            # Add specific field errors to messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field.replace("_", " ").title()}: {error}')
    else:
        # GET request - initialize form with current user's data
        initial_data = {
            'first_name': current_user.first_name or '',
            'last_name': current_user.last_name or '',
            'email': current_user.email or '',
            'phone': profile.phone or '',
            'assigned_architect': profile.assigned_architect or '',
            'project_name': profile.project_name or '',
            'project_start': profile.project_start or '',
        }
        
        print(f"[DEBUG] USERSETTINGS - Initial form data: {initial_data}")
        form = ProfileUpdateForm(instance=profile, user=current_user, initial=initial_data)
    
    # SECURITY: Only pass current user's data to template
    context = {
        'profile': profile,
        'form': form,
        'user': current_user,  # Explicitly pass current user
        'user_full_name': current_user.get_full_name() or current_user.username,
        'user_email': current_user.email,
        'profile_role': profile.role.title() if profile.role else 'Customer',
        # Additional user-specific data
        'account_created': current_user.date_joined.strftime('%B %d, %Y') if current_user.date_joined else 'Unknown',
        'last_login': current_user.last_login.strftime('%B %d, %Y at %I:%M %p') if current_user.last_login else 'Never',
        'account_status': 'Active' if current_user.is_active else 'Inactive',
        'user_id': current_user.id,
    }
    
    print(f"[DEBUG] USERSETTINGS - Rendering template for user: {current_user.username}")
    
    # Add cache-busting timestamp
    import time
    context['cache_buster'] = int(time.time())
    
    response = render(request, 'core/usersettings.html', context)
    
    # Add headers to prevent caching
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    
    return response

def login(request):
    return render(request, 'core/login.html')