#!/usr/bin/env python
import os
import sys
import django
from django.conf import settings

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.urls import reverse, resolve
from django.test import Client

def test_admin_urls():
    print("Testing Admin URLs...")
    
    try:
        # Test URL reverse
        admin_login_url = reverse('accounts:admin_login')
        print(f"✓ Admin login URL: {admin_login_url}")
        
        admin_register_url = reverse('accounts:admin_register')
        print(f"✓ Admin register URL: {admin_register_url}")
        
        # Test URL resolution
        resolver = resolve('/accounts/admin-auth/login/')
        print(f"✓ URL resolves to: {resolver.func.__name__}")
        print(f"✓ View module: {resolver.func.__module__}")
        
        # Test with client
        client = Client()
        response = client.get('/accounts/admin-auth/login/')
        print(f"✓ Response status: {response.status_code}")
        print(f"✓ Response contains 'login': {'login' in response.content.decode().lower()}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

if __name__ == '__main__':
    test_admin_urls()
