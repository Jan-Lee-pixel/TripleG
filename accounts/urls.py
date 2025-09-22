from django.urls import path
from . import views

urlpatterns = [
    # Admin
    path('admin/login/', views.admin_login_view, name='admin_login'),
    path('admin/register/', views.admin_register_view, name='admin_register'),

    # Client
    path('client/login/', views.client_login_view, name='client_login'),
    path('client/register/', views.client_register_view, name='client_register'),

    # Sitemanger
    path('sitemanger/login/', views.sitemanger_login_view, name='sitemanger_login'),
    path('sitemanger/register/', views.sitemanger_register_view, name='sitemanger_register'),
]