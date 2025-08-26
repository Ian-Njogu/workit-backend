from django.contrib import admin
from .models import Application

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'worker', 'quote', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('job__title', 'worker__email', 'message')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Application', {'fields': ('job', 'worker', 'message', 'quote')}),
        ('Status', {'fields': ('status',)}),
        ('Timestamps', {'fields': ('created_at',)}),
    )
    
    readonly_fields = ('created_at',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('job', 'worker')
