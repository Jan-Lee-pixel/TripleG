from django.shortcuts import render

def chatbot(request):
    return render(request, 'chatbot/chatbot.html')

def adminmessagecenter(request):
    return render(request, 'admin/adminmessagecenter.html')

