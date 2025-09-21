from django.shortcuts import render

# Create your views here.

def projectmanagement(request):
 
   return render(request, 'admin/projectmanagement.html')

def project_list(request):
    # Placeholder for now
    return render(request, 'portfolio/project-list.html')

def project_detail(request, project_id):
    # In a real app, you'd fetch the project from the database
    # For now, just pass the project_id to the template
    return render(request, 'portfolio/project-detail.html', {'project_id': project_id})


