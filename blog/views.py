from django.shortcuts import render
from accounts.decorators import require_admin_role, allow_public_access

# Create your views here.

@require_admin_role
def blog_management(request):
    return render(request, 'admin/blogmanagement.html')

@allow_public_access
def blog_list(request):
    return render(request, 'bloguser/bloglist.html')

@allow_public_access
def blog_individual(request, blog_id=None):
    # blog_id is optional for now; you can make it required if you want
    return render(request, 'bloguser/blogindividualpage.html', {'blog_id': blog_id})
