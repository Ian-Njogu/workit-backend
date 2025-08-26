from django.contrib import admin
from .models import WorkerProfile

@admin.register(WorkerProfile)
class WorkerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'location', 'hourly_rate', 'rating', 'review_count', 'available')
    list_filter = ('category', 'location', 'available', 'rating')
    search_fields = ('user__email', 'user__name', 'category', 'location')
    ordering = ('-rating', '-review_count')
    
    fieldsets = (
        ('User', {'fields': ('user',)}),
        ('Profile', {'fields': ('category', 'location', 'hourly_rate', 'available')}),
        ('Performance', {'fields': ('rating', 'review_count')}),
        ('Details', {'fields': ('skills', 'portfolio')}),
    )
    
    readonly_fields = ('rating', 'review_count')
