from django.urls import path
from django.shortcuts import redirect
from . import views

app_name = 'core'

def user_dashboard_redirect(request):
    """Redirect /user/ to /usersettings/ for backward compatibility"""
    return redirect('core:usersettings')

urlpatterns = [
    path('', views.home, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('project/', views.project, name='project'),
    path('usersettings/', views.usersettings, name='usersettings'),
    path('user/', user_dashboard_redirect, name='user_dashboard'),  # Redirect for backward compatibility
]