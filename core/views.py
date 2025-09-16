from django.shortcuts import render

def home(request):
    return render(request, 'core/home.html')

def about(request):
    return render(request, 'core/aboutus.html')

def contact(request):
    return render(request, 'core/contacts.html')

def project(request):
    return render(request, 'core/project.html')

def usersettings(request):
    return render(request, 'core/usersettings.html')

def login(request):
    return render(request, 'core/login.html')