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
from .models import (
    Project, DiaryEntry, LaborEntry, MaterialEntry, 
    EquipmentEntry, DelayEntry, VisitorEntry, DiaryPhoto
)
from .forms import (
    ProjectForm, DiaryEntryForm, LaborEntryFormSet, MaterialEntryFormSet,
    EquipmentEntryFormSet, DelayEntryFormSet, VisitorEntryFormSet,
    DiaryPhotoFormSet, DiarySearchForm, ProjectSearchForm
)
from .utils import get_user_projects, get_project_statistics

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

def createblog(request):
    return render(request, 'blogcreation/createblog.html')

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
def export_reports(request):
    """Export reports to CSV format"""
    # Get user's projects
    if request.user.is_staff:
        projects = Project.objects.all()
    else:
        projects = Project.objects.filter(
            Q(project_manager=request.user) | Q(architect=request.user)
        )
    
    export_type = request.GET.get('type', 'summary')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    selected_project = request.GET.get('project')
    
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
    
    response = HttpResponse(content_type='text/csv')
    
    if export_type == 'summary':
        response['Content-Disposition'] = 'attachment; filename="project_summary_report.csv"'
        writer = csv.writer(response)
        writer.writerow([
            'Project Name', 'Client', 'Status', 'Entries Count', 'Total Delays', 
            'Total Delay Hours', 'Labor Cost', 'Material Cost', 'Equipment Cost', 
            'Total Cost', 'Avg Progress %', 'Safety Incidents', 'Quality Issues'
        ])
        
        for project in projects:
            project_entries = entries.filter(project=project)
            labor_entries = LaborEntry.objects.filter(diary_entry__in=project_entries)
            material_entries = MaterialEntry.objects.filter(diary_entry__in=project_entries)
            equipment_entries = EquipmentEntry.objects.filter(diary_entry__in=project_entries)
            delay_entries = DelayEntry.objects.filter(diary_entry__in=project_entries)
            
            total_labor_cost = sum(labor.total_cost for labor in labor_entries)
            total_material_cost = sum(material.total_cost for material in material_entries)
            total_equipment_cost = sum(equipment.total_rental_cost for equipment in equipment_entries)
            
            progress_data = project_entries.aggregate(avg_progress=Avg('progress_percentage'))
            safety_incidents = project_entries.exclude(safety_incidents='').count()
            quality_issues = project_entries.exclude(quality_issues='').count()
            
            writer.writerow([
                project.name,
                project.client_name,
                project.get_status_display(),
                project_entries.count(),
                delay_entries.count(),
                delay_entries.aggregate(total=Sum('duration_hours'))['total'] or 0,
                total_labor_cost,
                total_material_cost,
                total_equipment_cost,
                total_labor_cost + total_material_cost + total_equipment_cost,
                round(progress_data['avg_progress'] or 0, 2),
                safety_incidents,
                quality_issues
            ])
    
    elif export_type == 'delays':
        response['Content-Disposition'] = 'attachment; filename="delays_report.csv"'
        writer = csv.writer(response)
        writer.writerow([
            'Date', 'Project', 'Delay Category', 'Description', 'Duration Hours', 
            'Cost Impact', 'Responsible Party', 'Created By'
        ])
        
        delay_entries = DelayEntry.objects.filter(diary_entry__in=entries).select_related(
            'diary_entry__project', 'diary_entry__created_by'
        )
        
        for delay in delay_entries:
            writer.writerow([
                delay.diary_entry.entry_date,
                delay.diary_entry.project.name,
                delay.get_category_display(),
                delay.description,
                delay.duration_hours,
                delay.cost_impact,
                delay.responsible_party,
                delay.diary_entry.created_by.get_full_name() or delay.diary_entry.created_by.username
            ])
    
    elif export_type == 'labor':
        response['Content-Disposition'] = 'attachment; filename="labor_report.csv"'
        writer = csv.writer(response)
        writer.writerow([
            'Date', 'Project', 'Labor Type', 'Workers Count', 'Hours Worked', 
            'Overtime Hours', 'Hourly Rate', 'Total Cost', 'Tasks Completed'
        ])
        
        labor_entries = LaborEntry.objects.filter(diary_entry__in=entries).select_related(
            'diary_entry__project'
        )
        
        for labor in labor_entries:
            writer.writerow([
                labor.diary_entry.entry_date,
                labor.diary_entry.project.name,
                labor.get_labor_type_display(),
                labor.workers_count,
                labor.hours_worked,
                labor.overtime_hours,
                labor.hourly_rate,
                labor.total_cost,
                labor.tasks_completed
            ])
    
    elif export_type == 'materials':
        response['Content-Disposition'] = 'attachment; filename="materials_report.csv"'
        writer = csv.writer(response)
        writer.writerow([
            'Date', 'Project', 'Material Name', 'Supplier', 'Quantity Delivered', 
            'Quantity Used', 'Unit Cost', 'Total Cost', 'Storage Location'
        ])
        
        material_entries = MaterialEntry.objects.filter(diary_entry__in=entries).select_related(
            'diary_entry__project'
        )
        
        for material in material_entries:
            writer.writerow([
                material.diary_entry.entry_date,
                material.diary_entry.project.name,
                material.material_name,
                material.supplier,
                material.quantity_delivered,
                material.quantity_used,
                material.unit_cost,
                material.total_cost,
                material.storage_location
            ])
    
    return response

@login_required
def settings(request):
    """User settings and preferences"""
    return render(request, 'site_diary/settings.html')

# Admin views
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
def adminclientdiary(request):
    """Admin view for client diary entries"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('dashboard')
    
    # Get all diary entries with related data
    entries = DiaryEntry.objects.all().select_related(
        'project', 'created_by', 'reviewed_by'
    ).prefetch_related(
        'labor_entries', 'material_entries', 'equipment_entries',
        'delay_entries', 'visitor_entries', 'photos'
    ).order_by('-entry_date')
    
    # Apply search filters
    search_query = request.GET.get('search', '')
    if search_query:
        entries = entries.filter(
            Q(project__name__icontains=search_query) |
            Q(work_description__icontains=search_query) |
            Q(created_by__username__icontains=search_query)
        )
    
    # Filter by approval status
    status_filter = request.GET.get('status', '')
    if status_filter == 'approved':
        entries = entries.filter(approved=True)
    elif status_filter == 'pending':
        entries = entries.filter(approved=False)
    
    # Filter by project
    project_filter = request.GET.get('project', '')
    if project_filter:
        try:
            entries = entries.filter(project_id=int(project_filter))
        except (ValueError, TypeError):
            pass
    
    # Pagination
    paginator = Paginator(entries, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get projects for filter dropdown
    projects = Project.objects.all().order_by('name')
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'project_filter': project_filter,
        'projects': projects,
    }
    return render(request, 'admin/adminclientdiary.html', context)

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
    """Site draft entries with enhanced functionality"""
    # Get user's projects
    if request.user.is_staff:
        projects = Project.objects.all()
    else:
        projects = Project.objects.filter(
            Q(project_manager=request.user) | Q(architect=request.user)
        )
    
    # Get draft entries (not approved) with all related data
    draft_entries = DiaryEntry.objects.filter(
        project__in=projects,
        approved=False
    ).select_related('project', 'created_by').prefetch_related(
        'labor_entries', 'material_entries', 'equipment_entries', 
        'delay_entries', 'visitor_entries', 'photos'
    ).order_by('-created_at')
    
    # Apply search filter if provided
    search_query = request.GET.get('search', '')
    if search_query:
        draft_entries = draft_entries.filter(
            Q(work_description__icontains=search_query) |
            Q(project__name__icontains=search_query) |
            Q(general_notes__icontains=search_query)
        )
    
    # Calculate summary statistics
    total_drafts = draft_entries.count()
    my_drafts = draft_entries.filter(created_by=request.user).count()
    recent_drafts = draft_entries.filter(
        created_at__gte=timezone.now() - timedelta(days=7)
    ).count()
    
    # Pagination
    paginator = Paginator(draft_entries, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'summary_stats': {
            'total_drafts': total_drafts,
            'my_drafts': my_drafts,
            'recent_drafts': recent_drafts,
        }
    }
    return render(request, 'site_diary/sitedraft.html', context)

# Entry detail and edit views
@login_required
def entry_detail(request, entry_id):
    """View complete diary entry with all related data"""
    entry = get_object_or_404(DiaryEntry, id=entry_id)
    
    # Check permissions
    if not request.user.is_staff:
        user_projects = get_user_projects(request.user)
        if entry.project not in user_projects:
            messages.error(request, 'Access denied.')
            return redirect('history')
    
    # Get all related data
    labor_entries = entry.labor_entries.all()
    material_entries = entry.material_entries.all()
    equipment_entries = entry.equipment_entries.all()
    delay_entries = entry.delay_entries.all()
    visitor_entries = entry.visitor_entries.all()
    photos = entry.photos.all()
    
    # Calculate totals
    total_labor_cost = sum(labor.total_cost for labor in labor_entries)
    total_material_cost = sum(material.total_cost for material in material_entries)
    total_equipment_cost = sum(equipment.total_rental_cost for equipment in equipment_entries)
    total_delay_hours = sum(delay.duration_hours for delay in delay_entries)
    
    context = {
        'entry': entry,
        'labor_entries': labor_entries,
        'material_entries': material_entries,
        'equipment_entries': equipment_entries,
        'delay_entries': delay_entries,
        'visitor_entries': visitor_entries,
        'photos': photos,
        'totals': {
            'labor_cost': total_labor_cost,
            'material_cost': total_material_cost,
            'equipment_cost': total_equipment_cost,
            'total_cost': total_labor_cost + total_material_cost + total_equipment_cost,
            'delay_hours': total_delay_hours,
        }
    }
    return render(request, 'site_diary/entry_detail.html', context)

@login_required
def entry_edit(request, entry_id):
    """Edit diary entry"""
    entry = get_object_or_404(DiaryEntry, id=entry_id)
    
    # Check permissions
    if not request.user.is_staff:
        user_projects = get_user_projects(request.user)
        if entry.project not in user_projects:
            messages.error(request, 'Access denied.')
            return redirect('history')
        # Only allow editing own entries or if user is project manager/architect
        if (entry.created_by != request.user and 
            entry.project.project_manager != request.user and 
            entry.project.architect != request.user):
            messages.error(request, 'You can only edit your own entries.')
            return redirect('history')
    
    if request.method == 'POST':
        diary_form = DiaryEntryForm(request.POST, instance=entry)
        
        if diary_form.is_valid():
            diary_form.save()
            messages.success(request, 'Diary entry updated successfully!')
            return redirect('entry_detail', entry_id=entry.id)
    else:
        diary_form = DiaryEntryForm(instance=entry)
    
    context = {
        'entry': entry,
        'diary_form': diary_form,
        'is_edit': True
    }
    return render(request, 'site_diary/diary.html', context)

@login_required
def entry_delete(request, entry_id):
    """Delete diary entry (only drafts)"""
    entry = get_object_or_404(DiaryEntry, id=entry_id)
    
    # Check permissions
    if not request.user.is_staff:
        user_projects = get_user_projects(request.user)
        if entry.project not in user_projects:
            messages.error(request, 'Access denied.')
            return redirect('sitedraft')
        # Only allow deleting own entries
        if entry.created_by != request.user:
            messages.error(request, 'You can only delete your own entries.')
            return redirect('sitedraft')
    
    # Only allow deleting draft entries (not approved)
    if entry.approved:
        messages.error(request, 'Cannot delete approved entries.')
        return redirect('history')
    
    if request.method == 'POST':
        project_name = entry.project.name
        entry_date = entry.entry_date
        entry.delete()
        messages.success(request, f'Draft entry for {project_name} on {entry_date} deleted successfully.')
        return redirect('sitedraft')
    
    context = {'entry': entry}
    return render(request, 'site_diary/entry_confirm_delete.html', context)

# API endpoints for AJAX requests
@login_required
def approve_entry(request, entry_id):
    """Approve a diary entry"""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    entry = get_object_or_404(DiaryEntry, id=entry_id)
    entry.approved = True
    entry.reviewed_by = request.user
    entry.approval_date = timezone.now()
    entry.save()
    
    return JsonResponse({'success': True, 'message': 'Entry approved successfully'})

@login_required
def get_project_details(request, project_id):
    """Get project details for AJAX requests"""
    project = get_object_or_404(Project, id=project_id)
    
    # Check if user has access to this project
    if not request.user.is_staff:
        if project.project_manager != request.user and project.architect != request.user:
            return JsonResponse({'error': 'Access denied'}, status=403)
    
    data = {
        'name': project.name,
        'client_name': project.client_name,
        'location': project.location,
        'status': project.get_status_display(),
        'progress': project.diary_entries.aggregate(
            avg_progress=Avg('progress_percentage')
        )['avg_progress'] or 0
    }
    
    return JsonResponse(data)