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

from django.urls import get_resolver
from django.test import Client
from django.http import HttpRequest

def debug_url_patterns():
    print("=== DEBUGGING URL PATTERNS ===")
    
    # Get the root URL resolver
    resolver = get_resolver()
    
    print("\n1. ROOT URL PATTERNS:")
    for pattern in resolver.url_patterns:
        print(f"   {pattern.pattern} -> {pattern}")
    
    print("\n2. ACCOUNTS URL PATTERNS:")
    for pattern in resolver.url_patterns:
        if hasattr(pattern, 'namespace') and pattern.namespace == 'accounts':
            print(f"   Found accounts namespace: {pattern}")
            for sub_pattern in pattern.url_patterns:
                print(f"     {sub_pattern.pattern} -> {sub_pattern.callback}")
    
    print("\n3. TESTING SPECIFIC URL:")
    try:
        from django.urls import resolve
        match = resolve('/accounts/admin-auth/login/')
        print(f"   URL: /accounts/admin-auth/login/")
        print(f"   View: {match.func}")
        print(f"   View Name: {match.view_name}")
        print(f"   Namespace: {match.namespace}")
        print(f"   URL Name: {match.url_name}")
    except Exception as e:
        print(f"   ERROR: {e}")
    
    print("\n4. TESTING WITH CLIENT:")
    client = Client()
    try:
        response = client.get('/accounts/admin-auth/login/', HTTP_HOST='127.0.0.1:8000')
        print(f"   Status: {response.status_code}")
        content = response.content.decode()
        print(f"   Contains 'Django administration': {'Django administration' in content}")
        print(f"   Contains 'Triple G': {'Triple G' in content}")
        print(f"   Contains 'admin_login_view': {'admin_login_view' in content}")
        print(f"   First 200 chars: {content[:200]}")
    except Exception as e:
        print(f"   ERROR: {e}")

if __name__ == '__main__':
    debug_url_patterns()
