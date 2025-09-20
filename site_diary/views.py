from django.shortcuts import render

# Create your views here.
def diary(request):
    return render(request, 'site_diary/diary.html')

def dashboard(request):
    return render(request, 'site_diary/dashboard.html')

def chatbot(request):
    return render(request, 'chatbot/chatbot.html')

def newproject(request):
    return render(request, 'site_diary/newproject.html')

def createblog(request):
    return render(request, 'blogcreation/createblog.html')

def drafts(request):
    return render(request, 'blogcreation/drafts.html')

def history(request):
    return render(request, 'site_diary/history.html')

def reports(request):
    return render(request, 'site_diary/reports.html')

def settings(request):
    return render(request, 'site_diary/settings.html')

def sitedraft(request):
    return render(request, 'sitedraft.html')