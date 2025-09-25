from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db.models import Q, Sum, Avg, Count, Max, Min
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta
import csv
import json
from accounts.decorators import require_site_manager_role, require_admin_role

# Create your views here.
@login_required
def diary(request):
    """Create new diary entry with all related data"""
    if request.method == 'POST':
        diary_form = DiaryEntryForm(request.POST)
        labor_formset = LaborEntryFormSet(request.POST, prefix='labor')
        material_formset = MaterialEntryFormSet(request.POST, prefix='material')
        equipment_formset = EquipmentEntryFormSet(request.POST, prefix='equipment')
        delay_formset = DelayEntryFormSet(request.POST, prefix='delay')
        visitor_formset = VisitorEntryFormSet(request.POST, prefix='visitor')
        photo_formset = DiaryPhotoFormSet(request.POST, request.FILES, prefix='photo')
        
        if (diary_form.is_valid() and labor_formset.is_valid() and 
            material_formset.is_valid() and equipment_formset.is_valid() and
            delay_formset.is_valid() and visitor_formset.is_valid() and
            photo_formset.is_valid()):
            
            # Save diary entry
            diary_entry = diary_form.save(commit=False)
            diary_entry.created_by = request.user
            diary_entry.save()
            
            # Save related entries
            for form in labor_formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    labor_entry = form.save(commit=False)
                    labor_entry.diary_entry = diary_entry
                    labor_entry.save()
            
            for form in material_formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    material_entry = form.save(commit=False)
                    material_entry.diary_entry = diary_entry
                    material_entry.save()
            
            for form in equipment_formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    equipment_entry = form.save(commit=False)
                    equipment_entry.diary_entry = diary_entry
                    equipment_entry.save()
            
            for form in delay_formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    delay_entry = form.save(commit=False)
                    delay_entry.diary_entry = diary_entry
                    delay_entry.save()
            
            for form in visitor_formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    visitor_entry = form.save(commit=False)
                    visitor_entry.diary_entry = diary_entry
                    visitor_entry.save()
            
            for form in photo_formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    photo_entry = form.save(commit=False)
                    photo_entry.diary_entry = diary_entry
                    photo_entry.save()
            
            messages.success(request, 'Diary entry created successfully!')
            return redirect('diary')
    else:
        diary_form = DiaryEntryForm()
        labor_formset = LaborEntryFormSet(prefix='labor')
        material_formset = MaterialEntryFormSet(prefix='material')
        equipment_formset = EquipmentEntryFormSet(prefix='equipment')
        delay_formset = DelayEntryFormSet(prefix='delay')
        visitor_formset = VisitorEntryFormSet(prefix='visitor')
        photo_formset = DiaryPhotoFormSet(prefix='photo')
    
    context = {
        'diary_form': diary_form,
        'labor_formset': labor_formset,
        'material_formset': material_formset,
        'equipment_formset': equipment_formset,
        'delay_formset': delay_formset,
        'visitor_formset': visitor_formset,
        'photo_formset': photo_formset,
    }
    return render(request, 'site_diary/diary.html', context)

@login_required
def dashboard(request):
    """Dashboard with project overview and statistics"""
    # Get user's projects
    if request.user.is_staff:
        projects = Project.objects.all()
    else:
        projects = Project.objects.filter(
            Q(project_manager=request.user) | Q(architect=request.user)
        )
    
    # Recent diary entries
    recent_entries = DiaryEntry.objects.filter(
        project__in=projects
    ).select_related('project', 'created_by').order_by('-created_at')[:5]
    
    # Statistics
    total_projects = projects.count()
    active_projects = projects.filter(status='active').count()
    completed_projects = projects.filter(status='completed').count()
    total_entries = DiaryEntry.objects.filter(project__in=projects).count()
    
    # Recent delays
    recent_delays = DelayEntry.objects.filter(
        diary_entry__project__in=projects
    ).select_related('diary_entry__project').order_by('-diary_entry__entry_date')[:5]
    
    context = {
        'projects': projects[:5],  # Show only 5 recent projects
        'recent_entries': recent_entries,
        'recent_delays': recent_delays,
        'stats': {
            'total_projects': total_projects,
            'active_projects': active_projects,
            'completed_projects': completed_projects,
            'total_entries': total_entries,
        }
    }
    return render(request, 'site_diary/dashboard.html', context)

@require_site_manager_role
def chatbot(request):
    return render(request, 'chatbot/chatbot.html')

@login_required
def newproject(request):
    """Create new project"""
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            messages.success(request, f'Project "{project.name}" created successfully!')
            return redirect('dashboard')
    else:
        form = ProjectForm()
    
    context = {'form': form}
    return render(request, 'site_diary/newproject.html', context)

@require_site_manager_role
def createblog(request):
    return render(request, 'blogcreation/createblog.html')

@require_site_manager_role
def drafts(request):
    return render(request, 'blogcreation/drafts.html')

@login_required
def history(request):
    """View diary entry history with search and filtering"""
    # Get user's projects
    if request.user.is_staff:
        projects = Project.objects.all()
    else:
        projects = Project.objects.filter(
            Q(project_manager=request.user) | Q(architect=request.user)
        )
    
    # Get diary entries
    entries = DiaryEntry.objects.filter(project__in=projects).select_related(
        'project', 'created_by', 'reviewed_by'
    ).prefetch_related('labor_entries', 'material_entries', 'equipment_entries')
    
    # Apply search filters
    search_form = DiarySearchForm(request.GET)
    if search_form.is_valid():
        if search_form.cleaned_data['project']:
            entries = entries.filter(project=search_form.cleaned_data['project'])
        if search_form.cleaned_data['start_date']:
            entries = entries.filter(entry_date__gte=search_form.cleaned_data['start_date'])
        if search_form.cleaned_data['end_date']:
            entries = entries.filter(entry_date__lte=search_form.cleaned_data['end_date'])
        if search_form.cleaned_data['weather_condition']:
            entries = entries.filter(weather_condition=search_form.cleaned_data['weather_condition'])
        if search_form.cleaned_data['created_by']:
            entries = entries.filter(created_by=search_form.cleaned_data['created_by'])
    
    # Pagination
    paginator = Paginator(entries.order_by('-entry_date'), 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_form': search_form,
    }
    return render(request, 'site_diary/history.html', context)

@login_required
def reports(request):
    """Generate comprehensive reports and analytics with database data"""
    # Get user's projects
    if request.user.is_staff:
        projects = Project.objects.all()
    else:
        projects = Project.objects.filter(
            Q(project_manager=request.user) | Q(architect=request.user)
        )
    
    # Date filtering
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    selected_project = request.GET.get('project')
    report_type = request.GET.get('report_type', 'summary')
    
    # Filter projects if specific project selected
    if selected_project:
        try:
            projects = projects.filter(id=int(selected_project))
        except (ValueError, TypeError):
            pass
    
    # Get diary entries for the period
    entries = DiaryEntry.objects.filter(project__in=projects)
    if start_date:
        entries = entries.filter(entry_date__gte=start_date)
    if end_date:
        entries = entries.filter(entry_date__lte=end_date)
    
    # Project statistics with comprehensive data from database
    project_stats = []
    for project in projects:
        project_entries = entries.filter(project=project)
        
        # Get all related data for this project from database
        labor_entries = LaborEntry.objects.filter(diary_entry__in=project_entries)
        material_entries = MaterialEntry.objects.filter(diary_entry__in=project_entries)
        equipment_entries = EquipmentEntry.objects.filter(diary_entry__in=project_entries)
        delay_entries = DelayEntry.objects.filter(diary_entry__in=project_entries)
        visitor_entries = VisitorEntry.objects.filter(diary_entry__in=project_entries)
        
        # Calculate costs from database
        total_labor_cost = sum(labor.total_cost for labor in labor_entries)
        total_material_cost = sum(material.total_cost for material in material_entries)
        total_equipment_cost = sum(equipment.total_rental_cost for equipment in equipment_entries)
        total_delay_impact = delay_entries.aggregate(total=Sum('cost_impact'))['total'] or 0
        
        # Progress tracking from database
        progress_data = project_entries.aggregate(
            avg_progress=Avg('progress_percentage'),
            max_progress=Max('progress_percentage'),
            min_progress=Min('progress_percentage')
        )
        
        # Safety and quality metrics from database
        safety_incidents = project_entries.exclude(safety_incidents='').count()
        quality_issues = project_entries.exclude(quality_issues='').count()
        
        project_stats.append({
            'project': project,
            'entries_count': project_entries.count(),
            'total_delays': delay_entries.count(),
            'total_delay_hours': delay_entries.aggregate(total=Sum('duration_hours'))['total'] or 0,
            'total_labor_cost': total_labor_cost,
            'total_material_cost': total_material_cost,
            'total_equipment_cost': total_equipment_cost,
            'total_project_cost': total_labor_cost + total_material_cost + total_equipment_cost,
            'total_delay_impact': total_delay_impact,
            'avg_progress': progress_data['avg_progress'] or 0,
            'max_progress': progress_data['max_progress'] or 0,
            'min_progress': progress_data['min_progress'] or 0,
            'approved_entries': project_entries.filter(approved=True).count(),
            'pending_entries': project_entries.filter(approved=False).count(),
            'safety_incidents': safety_incidents,
            'quality_issues': quality_issues,
            'visitor_count': visitor_entries.count(),
            'photos_count': project_entries.filter(photos_taken=True).count(),
        })
    
    # Delay analysis by category from database
    delay_categories = DelayEntry.objects.filter(
        diary_entry__in=entries
    ).values('category').annotate(
        count=Count('id'),
        total_hours=Sum('duration_hours'),
        avg_impact=Avg('cost_impact'),
        total_cost_impact=Sum('cost_impact')
    ).order_by('-total_hours')
    
    # Weather analysis from database
    weather_stats = entries.exclude(weather_condition='').values('weather_condition').annotate(
        count=Count('id'),
        avg_temp_high=Avg('temperature_high'),
        avg_temp_low=Avg('temperature_low'),
        avg_humidity=Avg('humidity'),
        avg_wind_speed=Avg('wind_speed')
    ).order_by('-count')
    
    # Labor analysis from database
    labor_stats = LaborEntry.objects.filter(
        diary_entry__in=entries
    ).values('labor_type').annotate(
        total_workers=Sum('workers_count'),
        total_hours=Sum('hours_worked'),
        total_overtime=Sum('overtime_hours'),
        avg_hourly_rate=Avg('hourly_rate'),
        entry_count=Count('id')
    ).order_by('-total_hours')
    
    # Material analysis from database
    material_stats = MaterialEntry.objects.filter(
        diary_entry__in=entries
    ).values('material_name').annotate(
        total_delivered=Sum('quantity_delivered'),
        total_used=Sum('quantity_used'),
        avg_unit_cost=Avg('unit_cost'),
        total_entries=Count('id')
    ).order_by('-total_delivered')[:15]  # Top 15 materials
    
    # Equipment utilization from database
    equipment_stats = EquipmentEntry.objects.filter(
        diary_entry__in=entries
    ).values('equipment_type').annotate(
        total_hours=Sum('hours_operated'),
        avg_hourly_rate=Avg('rental_cost_per_hour'),
        total_fuel=Sum('fuel_consumption'),
        utilization_days=Count('diary_entry__entry_date', distinct=True),
        breakdown_count=Count('id', filter=Q(status='breakdown'))
    ).order_by('-total_hours')
    
    # Monthly progress tracking from database
    monthly_progress = entries.extra(
        select={'month': "DATE_TRUNC('month', entry_date)"}
    ).values('month').annotate(
        avg_progress=Avg('progress_percentage'),
        entry_count=Count('id'),
        total_delays=Count('delay_entries'),
        avg_temp=Avg('temperature_high')
    ).order_by('month')
    
    # Overall summary from database
    overall_summary = {
        'total_projects': projects.count(),
        'total_entries': entries.count(),
        'total_approved': entries.filter(approved=True).count(),
        'total_pending': entries.filter(approved=False).count(),
        'total_labor_entries': LaborEntry.objects.filter(diary_entry__in=entries).count(),
        'total_material_entries': MaterialEntry.objects.filter(diary_entry__in=entries).count(),
        'total_equipment_entries': EquipmentEntry.objects.filter(diary_entry__in=entries).count(),
        'total_delays': DelayEntry.objects.filter(diary_entry__in=entries).count(),
        'total_visitors': VisitorEntry.objects.filter(diary_entry__in=entries).count(),
        'date_range': {
            'start': start_date,
            'end': end_date,
        }
    }
    
    context = {
        'project_stats': project_stats,
        'delay_categories': delay_categories,
        'weather_stats': weather_stats,
        'labor_stats': labor_stats,
        'material_stats': material_stats,
        'equipment_stats': equipment_stats,
        'monthly_progress': monthly_progress,
        'overall_summary': overall_summary,
        'projects': Project.objects.filter(
            Q(project_manager=request.user) | Q(architect=request.user)
        ) if not request.user.is_staff else Project.objects.all(),
        'start_date': start_date,
        'end_date': end_date,
        'selected_project': selected_project,
        'report_type': report_type,
    }
    return render(request, 'site_diary/reports.html', context)

@login_required
def settings(request):
    """User settings and preferences"""
    return render(request, 'site_diary/settings.html')

@login_required
def adminclientproject(request):
    """Admin view for client projects"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('dashboard')
    
    search_form = ProjectSearchForm(request.GET)
    projects = Project.objects.all().select_related('project_manager', 'architect')
    
    if search_form.is_valid():
        if search_form.cleaned_data['name']:
            projects = projects.filter(name__icontains=search_form.cleaned_data['name'])
        if search_form.cleaned_data['client_name']:
            projects = projects.filter(client_name__icontains=search_form.cleaned_data['client_name'])
        if search_form.cleaned_data['status']:
            projects = projects.filter(status=search_form.cleaned_data['status'])
        if search_form.cleaned_data['project_manager']:
            projects = projects.filter(project_manager=search_form.cleaned_data['project_manager'])
    
    paginator = Paginator(projects.order_by('-created_at'), 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_form': search_form,
    }
    return render(request, 'admin/adminclientproject.html', context)

@login_required
def admindiary(request):
    """Admin view for diary entries"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('dashboard')
    
    entries = DiaryEntry.objects.all().select_related(
        'project', 'created_by', 'reviewed_by'
    ).order_by('-entry_date')
    
    paginator = Paginator(entries, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {'page_obj': page_obj}
    return render(request, 'admin/admindiary.html', context)

@login_required
def admindiaryreviewer(request):
    """Admin diary reviewer interface"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('dashboard')
    
    # Get entries pending review
    pending_entries = DiaryEntry.objects.filter(
        approved=False
    ).select_related('project', 'created_by').order_by('-entry_date')
    
    context = {'pending_entries': pending_entries}
    return render(request, 'admin/admindiaryreviewer.html', context)

@login_required
def adminhistory(request):
    """Admin history view"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('dashboard')
    
    return render(request, 'admin/adminhistory.html')

@login_required
def adminreports(request):
    """Admin reports view"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('dashboard')
    
    return render(request, 'admin/adminreports.html')

@login_required
def sitedraft(request):
    return render(request, 'site_diary/sitedraft.html')