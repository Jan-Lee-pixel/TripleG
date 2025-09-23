from django.urls import path, include
from . import views

urlpatterns = [
    # Client (with OTP functionality)
    path('client/login/', views.client_login_view, name='client_login'),
    path('client/register/', views.client_register_view, name='client_register'),
    path('client/verify-otp/', views.client_verify_otp, name='client_verify_otp'),
    path('client/resend-otp/', views.client_resend_otp, name='client_resend_otp'),
    path('client/logout/', views.client_logout_view, name='client_logout'),

    # Admin (with OTP functionality) - Changed to avoid Django admin conflicts
    path('admin-auth/login/', views.admin_login_view, name='admin_login'),
    path('admin-auth/register/', views.admin_register_view, name='admin_register'),
    path('admin-auth/verify-otp/', views.admin_verify_otp, name='admin_verify_otp'),
    path('admin-auth/resend-otp/', views.admin_resend_otp, name='admin_resend_otp'),
    path('admin-auth/logout/', views.admin_logout_view, name='admin_logout'),

    # Sitemanger (placeholder for now)
    path('sitemanger/login/', views.sitemanger_login_view, name='sitemanger_login'),
    path('sitemanger/register/', views.sitemanger_register_view, name='sitemanger_register'),
]