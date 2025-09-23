from django.shortcuts import render

# Create your views here.

def blog_management(request):
    return render(request, 'admin/blogmanagement.html')

def blog_list(request):
    return render(request, 'bloguser/bloglist.html')

def blog_individual(request, blog_id=None):
    # blog_id is optional for now; you can make it required if you want
    return render(request, 'bloguser/blogindividualpage.html', {'blog_id': blog_id})
