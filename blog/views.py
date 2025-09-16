from django.shortcuts import render

# Create your views here.

def blog_list(request):
    return render(request, 'blog/bloglist.html')

def blog_individual(request, blog_id=None):
    # blog_id is optional for now; you can make it required if you want
    return render(request, 'blog/blogindividualpage.html', {'blog_id': blog_id})
