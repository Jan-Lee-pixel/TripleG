
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from django.core.exceptions import ValidationError
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from .forms import ClientRegisterForm, OTPForm
from .models import OneTimePassword

# Client Registration with OTP
@csrf_protect
@never_cache
@transaction.atomic
def client_register_view(request):
    if request.method == "POST":
        form = ClientRegisterForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = form.save()
                    
                    # Generate OTP
                    code = OneTimePassword.generate_code()
                    OneTimePassword.objects.update_or_create(
                        user=user, 
                        defaults={"code": code}
                    )
                    
                    # Send OTP via email
                    print(f"[DEBUG] Sending OTP to: {user.email} from: {settings.DEFAULT_FROM_EMAIL} code: {code}")
                    result = send_mail(
                        "Verify your Triple G account",
                        f"Your OTP code is {code}. It will expire in 10 minutes.",
                        settings.DEFAULT_FROM_EMAIL,
                        [user.email],
                        fail_silently=False,
                    )
                    print(f"[DEBUG] send_mail result: {result}")
                    
                    messages.info(request, "Account created! Please verify with the OTP sent to your email.")
                    request.session['pending_user_id'] = user.id
                    return redirect("accounts:client_verify_otp")
                    
            except Exception as e:
                messages.error(request, "Error creating account or sending email. Please try again.")
                # Transaction will automatically rollback on exception
    else:
        form = ClientRegisterForm()
    return render(request, 'client/register.html', {"form": form})

# Client OTP Verification
@csrf_protect
@never_cache
@transaction.atomic
def client_verify_otp(request):
    user_id = request.session.get('pending_user_id')
    if not user_id:
        messages.error(request, "No pending verification found.")
        return redirect("accounts:client_register")
    
    try:
        user = User.objects.select_for_update().get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, "Invalid verification session.")
        return redirect("accounts:client_register")
    
    otp_obj = OneTimePassword.objects.filter(user=user).first()
    
    if request.method == "POST":
        form = OTPForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['otp']
            
            if otp_obj and otp_obj.code == code and not otp_obj.is_expired():
                with transaction.atomic():
                    user.is_active = True
                    user.save()
                    otp_obj.delete()
                    del request.session['pending_user_id']
                    
                messages.success(request, "Account verified! You can now log in.")
                return redirect("accounts:client_login")
            else:
                messages.error(request, "Invalid or expired OTP.")
    else:
        form = OTPForm()
    
    return render(request, "client/verify_otp.html", {"form": form, "email": user.email})

# Client Resend OTP
def client_resend_otp(request):
    user_id = request.session.get('pending_user_id')
    if not user_id:
        return redirect("accounts:client_register")
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return redirect("accounts:client_register")
    
    code = OneTimePassword.generate_code()
    OneTimePassword.objects.update_or_create(user=user, defaults={"code": code})
    
    try:
        send_mail(
            "Resend OTP - Triple G account",
            f"Your new OTP code is {code}. It will expire in 10 minutes.",
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        messages.success(request, "A new OTP has been sent to your email.")
    except Exception as e:
        messages.error(request, "Error sending email. Please try again.")
    
    return redirect("accounts:client_verify_otp")

# Client Login
@transaction.atomic
@csrf_protect
def client_login_view(request):
    reg_messages = []
    if request.method == "POST":
        # Check if this is a registration attempt
        if 'register' in request.POST:
            print("[DEBUG] Registration attempt detected")
            from django.contrib.auth.models import User
            from django.core.mail import send_mail
            from .models import OneTimePassword, Profile
            from django.db import IntegrityError

            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            password = request.POST.get('reg_password')
            username = email

            print(f"[DEBUG] Registration data - Name: {first_name} {last_name}, Email: {email}")

            if not all([first_name, last_name, email, password]):
                print("[DEBUG] Missing required fields")
                reg_messages.append({'tags': 'error', 'message': 'Please fill out all fields to register.'})
            # Remove this duplicate check since we handle it below
            # elif User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            #     print(f"[DEBUG] User already exists: {email}")
            #     reg_messages.append({'tags': 'error', 'message': 'This email is already registered. Please try logging in.'})
            else:
                try:
                    print("[DEBUG] Creating new user...")
                    with transaction.atomic():
                        # Check if user already exists (including inactive users)
                        existing_user = User.objects.filter(username=username).first()
                        if existing_user:
                            print(f"[DEBUG] User already exists: {existing_user.username} (Active: {existing_user.is_active})")
                            if not existing_user.is_active:
                                # Reactivate existing inactive user and resend OTP
                                user = existing_user
                                user.first_name = first_name
                                user.last_name = last_name
                                user.set_password(password)
                                user.save()
                                print(f"[DEBUG] Reactivated existing user: {user.username}")
                            else:
                                reg_messages.append({'tags': 'error', 'message': 'This email is already registered and active. Please try logging in.'})
                                return render(request, 'client/login.html', {'reg_messages': reg_messages})
                        else:
                            # Create new user
                            user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name, is_active=False)
                            print(f"[DEBUG] User created: {user.username} (ID: {user.id})")
                        
                        # Create profile manually (signal is disabled)
                        print(f"[DEBUG] Checking for existing profiles...")
                        existing_profiles = Profile.objects.filter(user=user)
                        print(f"[DEBUG] Found {existing_profiles.count()} existing profiles for user {user.id}")
                        
                        if existing_profiles.exists():
                            profile = existing_profiles.first()
                            print(f"[DEBUG] Using existing profile: {profile.id}")
                        else:
                            print(f"[DEBUG] Creating new profile for user: {user.username}")
                            profile = Profile.objects.create(user=user, role='customer')
                            print(f"[DEBUG] Profile created successfully: {profile.id}")
                        
                        code = OneTimePassword.generate_code()
                        OneTimePassword.objects.update_or_create(user=user, defaults={"code": code})
                        print(f"[DEBUG] OTP generated: {code}")
                        
                        send_mail(
                            "Verify your Triple G account",
                            f"Your OTP code is {code}. It will expire in 10 minutes.",
                            settings.DEFAULT_FROM_EMAIL,
                            [user.email],
                            fail_silently=False,
                        )
                        print(f"[DEBUG] OTP email sent to: {user.email}")
                        
                        request.session['pending_user_id'] = user.id
                        print(f"[DEBUG] Session set with user ID: {user.id}")
                        messages.info(request, "Account created! Please verify with the OTP sent to your email.")
                        print("[DEBUG] Redirecting to OTP verification...")
                        return redirect("accounts:client_verify_otp")
                except IntegrityError as e:
                    print(f"[DEBUG] IntegrityError: {e}")
                    reg_messages.append({'tags': 'error', 'message': 'Something went wrong on our end. Please try again.'})
                except Exception as e:
                    print(f"[DEBUG] Exception during registration: {e}")
                    reg_messages.append({'tags': 'error', 'message': 'An unexpected error occurred. Please try again shortly.'})
        
        # Handle login attempt
        else:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                if user.is_active:
                    login(request, user)
                    # The success message will be shown on the home page after redirect
                    messages.success(request, f"Welcome back, {user.first_name}!")
                    return redirect("core:index")
                else:
                    messages.warning(request, "Your account isn't active. Please check your email to verify your account.")
            else:
                # Use a generic message for security reasons
                messages.error(request, "The email or password you entered is incorrect.")
    return render(request, 'client/login.html', {'reg_messages': reg_messages})

# Client Logout
def client_logout_view(request):
    logout(request)
    messages.info(request, "You have been successfully logged out.")
    return redirect('accounts:client_login')

# Admin (placeholder views for now)
def admin_login_view(request):
    return render(request, 'admin/login.html')

def admin_register_view(request):
    return render(request, 'admin/register.html')

# Sitemanger (placeholder views for now)
def sitemanger_login_view(request):
    return render(request, 'sitemanger/login.html')

def sitemanger_register_view(request):
    return render(request, 'sitemanger/register.html')
