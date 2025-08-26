from django.contrib import admin
from .models import Job

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'client', 'worker', 'category', 'location', 'budget', 'status', 'created_at')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('title', 'description', 'client__email', 'worker__email')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Basic Info', {'fields': ('title', 'description', 'category', 'location')}),
        ('Financial', {'fields': ('budget', 'deadline')}),
        ('Assignment', {'fields': ('client', 'worker', 'status')}),
        ('Timestamps', {'fields': ('created_at',)}),
    )
    
    readonly_fields = ('created_at',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('client', 'worker')
