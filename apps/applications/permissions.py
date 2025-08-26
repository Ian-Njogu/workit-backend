from rest_framework import permissions

class IsApplicationOwner(permissions.BasePermission):
    """
    Allow access only to the worker who created the application.
    """
    def has_object_permission(self, request, view, obj):
        return obj.worker == request.user

class CanManageApplication(permissions.BasePermission):
    """
    Allow access only to the client who owns the job.
    """
    def has_object_permission(self, request, view, obj):
        return obj.job.client == request.user

class CanApplyToJob(permissions.BasePermission):
    """
    Allow workers to apply to jobs they haven't applied to yet.
    """
    def has_permission(self, request, view):
        if request.user.role != 'worker':
            return False
        
        # Check if worker already applied to this job
        job_id = view.kwargs.get('job_id')
        if job_id:
            from .models import Application
            return not Application.objects.filter(job_id=job_id, worker=request.user).exists()
        
        return True
