from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Prefetch
from django.core.paginator import Paginator
from django.http import Http404
from .models import Project, Category, ProjectImage, ProjectStat, ProjectTimeline

# Create your views here.

def projectmanagement(request):
    """Admin project management view"""
    return render(request, 'admin/projectmanagement.html')


def project_list(request):
    """Display list of projects with filtering and pagination"""
    # Get filter parameters
    year_filter = request.GET.get('year', 'all')
    category_filter = request.GET.get('category', 'all')
    search_query = request.GET.get('search', '').strip()
    
    # Start with all projects, optimizing queries
    projects = Project.objects.select_related('category').prefetch_related(
        Prefetch('images', queryset=ProjectImage.objects.order_by('order')[:1])
    )
    
    # Apply filters
    if year_filter != 'all':
        try:
            year = int(year_filter)
            projects = projects.filter(year=year)
        except (ValueError, TypeError):
            pass  # Invalid year, ignore filter
    
    if category_filter != 'all':
        if category_filter == 'featured':
            projects = projects.filter(featured=True)
        else:
            projects = projects.filter(category__slug=category_filter)
    
    # Apply search
    if search_query:
        projects = projects.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(location__icontains=search_query) |
            Q(lead_architect__icontains=search_query)
        )
    
    # Order projects
    projects = projects.order_by('-featured', '-completion_date', '-created_at')
    
    # Pagination
    paginator = Paginator(projects, 12)  # Show 12 projects per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get filter options for the template
    categories = Category.objects.all().order_by('name')
    years = Project.objects.values_list('year', flat=True).distinct().order_by('-year')
    
    context = {
        'page_obj': page_obj,
        'projects': page_obj,  # For template compatibility
        'categories': categories,
        'years': years,
        'current_year': year_filter,
        'current_category': category_filter,
        'search_query': search_query,
        'total_projects': paginator.count,
    }
    
    return render(request, 'portfolio/project-list.html', context)


def project_detail(request, project_id):
    """Display detailed view of a single project"""
    try:
        # Get project with all related data in optimized queries
        project = get_object_or_404(
            Project.objects.select_related('category').prefetch_related(
                Prefetch('images', queryset=ProjectImage.objects.order_by('order')),
                Prefetch('stats', queryset=ProjectStat.objects.order_by('order')),
                Prefetch('timeline', queryset=ProjectTimeline.objects.order_by('order'))
            ),
            id=project_id
        )
        
        # Get related projects (same category, excluding current)
        related_projects = Project.objects.filter(
            category=project.category
        ).exclude(id=project.id).select_related('category')[:3]
        
        context = {
            'project': project,
            'related_projects': related_projects,
            'project_images': project.images.all(),
            'project_stats': project.stats.all(),
            'project_timeline': project.timeline.all(),
        }
        
        return render(request, 'portfolio/project-detail.html', context)
        
    except Project.DoesNotExist:
        raise Http404("Project not found")
    except Exception as e:
        # Log the error in production
        # For now, raise Http404 for any unexpected errors
        raise Http404("Project not available")


