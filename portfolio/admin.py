from django.contrib import admin
from .models import Category, Project, ProjectImage, ProjectStat, ProjectTimeline

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    fields = ['image', 'alt_text', 'order']


class ProjectStatInline(admin.TabularInline):
    model = ProjectStat
    extra = 1
    fields = ['label', 'value', 'order']


class ProjectTimelineInline(admin.TabularInline):
    model = ProjectTimeline
    extra = 1
    fields = ['title', 'date', 'description', 'completed', 'order']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'year', 'status', 'featured', 'completion_date']
    list_filter = ['category', 'year', 'status', 'featured']
    search_fields = ['title', 'description', 'location', 'lead_architect']
    list_editable = ['featured', 'status']
    date_hierarchy = 'completion_date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'category')
        }),
        ('Project Details', {
            'fields': ('year', 'location', 'size', 'duration', 'completion_date', 'lead_architect')
        }),
        ('Status & Media', {
            'fields': ('status', 'featured', 'hero_image', 'video')
        }),
    )
    
    inlines = [ProjectImageInline, ProjectStatInline, ProjectTimelineInline]


@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ['project', 'alt_text', 'order']
    list_filter = ['project']
    ordering = ['project', 'order']


@admin.register(ProjectStat)
class ProjectStatAdmin(admin.ModelAdmin):
    list_display = ['project', 'label', 'value', 'order']
    list_filter = ['project', 'label']
    ordering = ['project', 'order']


@admin.register(ProjectTimeline)
class ProjectTimelineAdmin(admin.ModelAdmin):
    list_display = ['project', 'title', 'date', 'completed', 'order']
    list_filter = ['project', 'completed', 'date']
    date_hierarchy = 'date'
    ordering = ['project', 'order']
