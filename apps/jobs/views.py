from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Job
from .serializers import JobSerializer, JobCreateSerializer, JobFeedSerializer
from .permissions import IsJobOwner, CanUpdateJobStatus
from apps.applications.models import Application
from apps.applications.serializers import ApplicationCreateSerializer

class JobsViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing jobs.
    Supports CRUD operations with role-based permissions.
    """
    queryset = Job.objects.select_related('client', 'worker').all()
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated, IsJobOwner, CanUpdateJobStatus]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'category']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return JobCreateSerializer
        elif self.action == 'feed':
            return JobFeedSerializer
        return JobSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by client_id if provided
        client_id = self.request.query_params.get('client_id')
        if client_id:
            queryset = queryset.filter(client_id=client_id)
        
        # Filter by worker_id if provided
        worker_id = self.request.query_params.get('worker_id')
        if worker_id:
            queryset = queryset.filter(worker_id=worker_id)
        
        return queryset.order_by('-created_at')
    
    def perform_create(self, serializer):
        # Set the client from the authenticated user
        serializer.save(client=self.request.user)
    
    @action(detail=False, methods=['get'], url_path='feed')
    def feed(self, request):
        """
        Get jobs feed for workers (pending jobs they can apply to).
        """
        if request.user.role != 'worker':
            return Response(
                {"detail": "Only workers can access job feed"}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Get pending jobs that the worker hasn't applied to
        applied_job_ids = Application.objects.filter(
            worker=request.user
        ).values_list('job_id', flat=True)
        
        queryset = Job.objects.filter(
            status='pending'
        ).exclude(
            id__in=applied_job_ids
        ).select_related('client').order_by('-created_at')
        
        # Apply filters
        category = request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__icontains=category)
        
        location = request.query_params.get('location')
        if location:
            queryset = queryset.filter(location__icontains=location)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], url_path='applications')
    def applications(self, request, pk=None):
        """
        Allow a worker to apply to a job.
        """
        if request.user.role != 'worker':
            return Response(
                {"detail": "Only workers can apply to jobs"}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        job = self.get_object()
        
        # Check if job is available for applications
        if job.status != 'pending':
            return Response(
                {"detail": "Job is not available for applications"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if worker already applied
        if Application.objects.filter(job=job, worker=request.user).exists():
            return Response(
                {"detail": "You have already applied to this job"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = ApplicationCreateSerializer(
            data=request.data,
            context={'request': request, 'job_id': job.id}
        )
        
        if serializer.is_valid():
            Application.objects.create(
                job=job,
                worker=request.user,
                **serializer.validated_data
            )
            return Response(
                {"detail": "Application submitted successfully"}, 
                status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
