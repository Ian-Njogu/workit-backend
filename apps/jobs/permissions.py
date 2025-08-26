from rest_framework import permissions

class IsJobOwner(permissions.BasePermission):
    """
    Allow access only to the client who owns the job.
    """
    def has_object_permission(self, request, view, obj):
        return obj.client == request.user

class IsAssignedWorker(permissions.BasePermission):
    """
    Allow access only to the worker assigned to the job.
    """
    def has_object_permission(self, request, view, obj):
        return obj.worker == request.user

class CanUpdateJobStatus(permissions.BasePermission):
    """
    Allow status updates based on role and current status.
    """
    def has_object_permission(self, request, view, obj):
        if request.method not in ['PATCH', 'PUT']:
            return True
        
        # Only allow status updates
        if 'status' not in request.data:
            return True
        
        new_status = request.data['status']
        
        # Clients can update their own jobs
        if obj.client == request.user:
            return True
        
        # Workers can only update status on assigned jobs
        if obj.worker == request.user:
            allowed_transitions = {
                'accepted': ['in_progress'],
                'in_progress': ['completed']
            }
            return obj.status in allowed_transitions and new_status in allowed_transitions[obj.status]
        
        return False
