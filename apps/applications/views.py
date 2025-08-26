from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Application
from .serializers import ApplicationSerializer, ApplicationListSerializer
from .permissions import IsApplicationOwner, CanManageApplication, CanApplyToJob
from apps.jobs.models import Job

class ApplicationsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for managing job applications.
    Supports viewing applications with role-based filtering.
    """
    queryset = Application.objects.select_related('worker', 'job', 'job__client').all()
    serializer_class = ApplicationListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'job']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ApplicationSerializer
        return ApplicationListSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by client_id if provided (client viewing applications to their jobs)
        client_id = self.request.query_params.get('client_id')
        if client_id:
            queryset = queryset.filter(job__client_id=client_id)
        
        # Filter by job_id if provided
        job_id = self.request.query_params.get('job_id')
        if job_id:
            queryset = queryset.filter(job_id=job_id)
        
        # Workers can only see their own applications
        if self.request.user.role == 'worker':
            queryset = queryset.filter(worker=self.request.user)
        
        # Clients can only see applications to their jobs
        elif self.request.user.role == 'client':
            queryset = queryset.filter(job__client=self.request.user)
        
        return queryset.order_by('-created_at')
    
    @action(detail=True, methods=['post'], url_path='accept')
    def accept(self, request, pk=None):
        """
        Accept an application and assign the worker to the job.
        Only the job owner (client) can accept applications.
        """
        application = self.get_object()
        
        # Check if user can manage this application
        if not CanManageApplication().has_object_permission(request, self, application):
            return Response(
                {"detail": "You can only accept applications to your own jobs"}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Check if application is still pending
        if application.status != 'pending':
            return Response(
                {"detail": "Application is not pending"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if job is still available
        if application.job.status != 'pending':
            return Response(
                {"detail": "Job is not available for assignment"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Update application and job status
        application.status = 'accepted'
        application.save()
        
        application.job.status = 'accepted'
        application.job.worker = application.worker
        application.job.save()
        
        # Reject all other applications to this job
        Application.objects.filter(
            job=application.job,
            status='pending'
        ).exclude(id=application.id).update(status='rejected')
        
        return Response({
            "detail": "Application accepted successfully",
            "job_status": "accepted",
            "assigned_worker": application.worker.id
        })
    
    @action(detail=True, methods=['post'], url_path='reject')
    def reject(self, request, pk=None):
        """
        Reject an application.
        Only the job owner (client) can reject applications.
        """
        application = self.get_object()
        
        # Check if user can manage this application
        if not CanManageApplication().has_object_permission(request, self, application):
            return Response(
                {"detail": "You can only reject applications to your own jobs"}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Check if application is still pending
        if application.status != 'pending':
            return Response(
                {"detail": "Application is not pending"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Update application status
        application.status = 'rejected'
        application.save()
        
        return Response({"detail": "Application rejected successfully"})
