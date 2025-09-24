from django.shortcuts import render
from accounts.decorators import require_site_manager_role, require_admin_role

# Site Manager Views (supervisor role)
@require_site_manager_role
def diary(request):
    return render(request, 'site_diary/diary.html')

@require_site_manager_role
def dashboard(request):
    return render(request, 'site_diary/dashboard.html')

@require_site_manager_role
def chatbot(request):
    return render(request, 'chatbot/chatbot.html')

@require_site_manager_role
def newproject(request):
    return render(request, 'site_diary/newproject.html')

@require_site_manager_role
def createblog(request):
    return render(request, 'blogcreation/createblog.html')

@require_site_manager_role
def drafts(request):
    return render(request, 'blogcreation/drafts.html')

@require_site_manager_role
def history(request):
    return render(request, 'site_diary/history.html')

@require_site_manager_role
def reports(request):
    return render(request, 'site_diary/reports.html')

@require_site_manager_role
def settings(request):
    return render(request, 'site_diary/settings.html')

@require_site_manager_role
def sitedraft(request):
    return render(request, 'site_diary/sitedraft.html')

@require_site_manager_role
def project_detail(request, project_id):
    """
    Display detailed view of a specific project.
    For now, this renders with static data based on project_id.
    You can later integrate with a Project model when available.
    """
    # Static project data for demonstration
    # You can replace this with actual database queries later
    projects_data = {
        1: {
            'name': 'Harbor Tower',
            'status': 'ongoing',
            'location': 'Makati City, Philippines',
            'client': 'Harbor Development Corp.',
            'start_date': 'Jan 2024',
            'end_date': 'Dec 2025',
            'budget': '450,000,000',
            'progress': 65,
            'code': 'HT-2024-001',
            'type': 'Commercial',
            'architect': 'Arch. Maria Santos',
            'description': 'Luxury commercial building with 35 floors, featuring premium office spaces and retail outlets.'
        },
        2: {
            'name': 'Riverfront Promenade',
            'status': 'planning',
            'location': 'Cebu City, Philippines',
            'client': 'City Government of Cebu',
            'start_date': 'Mar 2024',
            'end_date': 'Nov 2025',
            'budget': '280,000,000',
            'progress': 40,
            'code': 'RP-2024-002',
            'type': 'Infrastructure',
            'architect': 'Arch. Juan Rodriguez',
            'description': 'Public infrastructure project featuring walkways, parks, and recreational areas along the river.'
        },
        3: {
            'name': 'Oakridge Residences',
            'status': 'ongoing',
            'location': 'Quezon City, Philippines',
            'client': 'Oakridge Development Inc.',
            'start_date': 'Sep 2023',
            'end_date': 'Jun 2025',
            'budget': '320,000,000',
            'progress': 85,
            'code': 'OR-2023-003',
            'type': 'Residential',
            'architect': 'Arch. Anna Cruz',
            'description': 'Luxury residential complex with 120 units, featuring modern amenities and green spaces.'
        },
        4: {
            'name': 'Tech Innovation Hub',
            'status': 'planning',
            'location': 'BGC, Taguig',
            'client': 'TechHub Philippines',
            'start_date': 'May 2024',
            'end_date': 'Dec 2026',
            'budget': '500,000,000',
            'progress': 25,
            'code': 'TH-2024-004',
            'type': 'Commercial',
            'architect': 'Arch. David Lee',
            'description': 'Modern facility designed for tech startups with co-working spaces, conference rooms, and labs.'
        },
        5: {
            'name': 'Central Hospital Extension',
            'status': 'ongoing',
            'location': 'Manila City',
            'client': 'Department of Health',
            'start_date': 'Feb 2024',
            'end_date': 'Aug 2025',
            'budget': '380,000,000',
            'progress': 55,
            'code': 'CH-2024-005',
            'type': 'Healthcare',
            'architect': 'Arch. Elena Santos',
            'description': 'Healthcare facility expansion with new emergency department, ICU, and specialized treatment areas.'
        },
        6: {
            'name': 'Sunset Mall Renovation',
            'status': 'ongoing',
            'location': 'Iloilo City',
            'client': 'Sunset Properties',
            'start_date': 'Jan 2024',
            'end_date': 'Oct 2025',
            'budget': '220,000,000',
            'progress': 75,
            'code': 'SM-2024-006',
            'type': 'Commercial',
            'architect': 'Arch. Miguel Torres',
            'description': 'Complete overhaul of existing mall with modern design, improved facilities, and expanded retail space.'
        }
    }
    
    # Get project data or use default
    project = projects_data.get(project_id, projects_data[1])  # Default to Harbor Tower
    
    context = {
        'project': project,
        'project_id': project_id,
    }
    
    return render(request, 'site_diary/site-project-detail.html', context)

# Admin Views (admin oversight of site diary)
@require_admin_role
def adminclientproject(request):
    return render(request, 'admin/adminclientproject.html')

@require_admin_role
def admindiary(request):
    return render(request, 'admin/admindiary.html')

@require_admin_role
def admindiaryreviewer(request):
    return render(request, 'admin/admindiaryreviewer.html')

@require_admin_role
def adminhistory(request):
    return render(request, 'admin/adminhistory.html')

@require_admin_role
def adminreports(request):
    return render(request, 'admin/adminreports.html')