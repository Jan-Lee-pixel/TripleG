from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from accounts.models import AdminProfile
from django.contrib.auth.models import User
from django.db.models import Count
import json

@login_required
def admin_home(request):
    """Admin dashboard home page"""
    # Check if user is admin/site manager
    try:
        admin_profile = AdminProfile.objects.get(user=request.user)
        if admin_profile.approval_status != 'approved':
            messages.error(request, 'Your admin account is not approved.')
            return redirect('accounts:client_login')
    except AdminProfile.DoesNotExist:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('accounts:client_login')
    
    # Get dashboard statistics
    context = {
        'total_users': User.objects.count(),
        'total_admins': AdminProfile.objects.filter(approval_status='approved').count(),
        'pending_approvals': AdminProfile.objects.filter(approval_status='pending').count(),
        'admin_profile': admin_profile,
        'user': request.user,
    }
    
    return render(request, 'adminhome.html', context)

@login_required
def admin_settings(request):
    """Admin settings page"""
    # Check if user is admin/site manager
    try:
        admin_profile = AdminProfile.objects.get(user=request.user)
        if admin_profile.approval_status != 'approved':
            messages.error(request, 'Your admin account is not approved.')
            return redirect('accounts:client_login')
    except AdminProfile.DoesNotExist:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('accounts:client_login')
    
    context = {
        'admin_profile': admin_profile,
        'user': request.user,
    }
    
    return render(request, 'adminsettings.html', context)

@login_required
@csrf_protect
@require_http_methods(["POST"])
def update_admin_settings(request):
    """Handle admin settings updates via AJAX"""
    try:
        admin_profile = AdminProfile.objects.get(user=request.user)
        if admin_profile.approval_status != 'approved':
            return JsonResponse({'success': False, 'message': 'Access denied.'})
    except AdminProfile.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Access denied.'})
    
    data = json.loads(request.body)
    section = data.get('section')
    
    if section == 'account':
        # Update user account information
        user = request.user
        user.email = data.get('email', user.email)
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.save()
        
        return JsonResponse({'success': True, 'message': 'Account updated successfully.'})
    
    elif section == 'security':
        # Update password
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        
        if not request.user.check_password(current_password):
            return JsonResponse({'success': False, 'message': 'Current password is incorrect.'})
        
        request.user.set_password(new_password)
        request.user.save()
        
        return JsonResponse({'success': True, 'message': 'Password updated successfully.'})
    
    elif section == 'system':
        # Handle system settings (you can extend this based on your needs)
        return JsonResponse({'success': True, 'message': 'System settings updated successfully.'})
    
    return JsonResponse({'success': False, 'message': 'Invalid section.'})

def admin_logout(request):
    """Admin logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('accounts:admin_login')
