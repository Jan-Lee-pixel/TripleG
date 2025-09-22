

# User Login View
from django.shortcuts import render

# Admin

def admin_login_view(request):
    return render(request, 'admin/login.html')

def admin_register_view(request):
    return render(request, 'admin/register.html')

# Client

def client_login_view(request):
    return render(request, 'client/login.html')

def client_register_view(request):
    return render(request, 'client/register.html')

# Sitemanger

def sitemanger_login_view(request):
    return render(request, 'sitemanger/login.html')

def sitemanger_register_view(request):
    return render(request, 'sitemanger/register.html')
