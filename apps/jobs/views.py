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
        
        # Filter by client_id if provided (matches mock API)
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
    
    def list(self, request, *args, **kwargs):
        """
        Override list to match mock API response format exactly.
        """
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        
        # Transform to match mock API response structure
        jobs_data = []
        for item in serializer.data:
            job_data = {
                'id': item['id'],
                'clientId': item['client']['id'],  # Mock has clientId
                'workerId': item['worker']['id'] if item['worker'] else None,  # Mock has workerId
                'title': item['title'],
                'description': item['description'],
                'category': item['category'],
                'location': item['location'],
                'budget': float(item['budget']),
                'deadline': item['deadline'],
                'status': item['status'],
                'createdAt': item['created_at'],  # Mock has createdAt
                'scheduledDate': None,  # Mock has scheduledDate
                'completedDate': None if item['status'] != 'completed' else item['created_at']  # Mock has completedDate
            }
            jobs_data.append(job_data)
        
        return Response(jobs_data)
    
    def retrieve(self, request, *args, **kwargs):
        """
        Override retrieve to match mock API response format exactly.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        
        # Transform to match mock API response structure
        job_data = {
            'id': data['id'],
            'clientId': data['client']['id'],
            'workerId': data['worker']['id'] if data['worker'] else None,
            'title': data['title'],
            'description': data['description'],
            'category': data['category'],
            'location': data['location'],
            'budget': float(data['budget']),
            'deadline': data['deadline'],
            'status': data['status'],
            'createdAt': data['created_at'],
            'scheduledDate': None,
            'completedDate': None if data['status'] != 'completed' else data['created_at']
        }
        
        return Response(job_data)
    
    @action(detail=False, methods=['get'], url_path='feed')
    def feed(self, request):
        """
        Get jobs feed for workers (pending jobs they can apply to).
        Matches mock API /api/v1/jobs?feed_for_worker_id=X
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
        
        serializer = self.get_serializer(queryset, many=True)
        
        # Transform to match mock API response structure
        jobs_data = []
        for item in serializer.data:
            job_data = {
                'id': item['id'],
                'clientId': item['client']['id'],
                'workerId': None,  # Feed jobs don't have workers assigned
                'title': item['title'],
                'description': item['description'],
                'category': item['category'],
                'location': item['location'],
                'budget': float(item['budget']),
                'deadline': item['deadline'],
                'status': item['status'],
                'createdAt': item['created_at'],
                'scheduledDate': None,
                'completedDate': None
            }
            jobs_data.append(job_data)
        
        return Response(jobs_data)
    
    @action(detail=True, methods=['post'], url_path='applications')
    def applications(self, request, pk=None):
        """
        Allow a worker to apply to a job.
        Matches mock API /api/v1/jobs/:id/applications
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
            application = Application.objects.create(
                job=job,
                worker=request.user,
                **serializer.validated_data
            )
            
            # Return response in mock API format
            response_data = {
                'id': application.id,
                'jobId': application.job.id,
                'workerId': application.worker.id,
                'message': application.message,
                'quote': float(application.quote),
                'status': application.status,
                'createdAt': application.created_at.isoformat()
            }
            
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'], url_path='invitations')
    def invitations(self, request, pk=None):
        """
        Client invites a worker to a job.
        Matches mock API /api/v1/jobs/:id/invitations
        """
        if request.user.role != 'client':
            return Response(
                {"detail": "Only clients can invite workers"}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        job = self.get_object()
        
        # Check if user owns the job
        if job.client != request.user:
            return Response(
                {"detail": "You can only invite workers to your own jobs"}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        worker_id = request.data.get('workerId')
        if not worker_id:
            return Response(
                {"detail": "workerId is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Update job with invited worker
        job.invited_worker_id = worker_id
        job.save()
        
        # Return updated job in mock API format
        serializer = self.get_serializer(job)
        data = serializer.data
        
        job_data = {
            'id': data['id'],
            'clientId': data['client']['id'],
            'workerId': data['worker']['id'] if data['worker'] else None,
            'title': data['title'],
            'description': data['description'],
            'category': data['category'],
            'location': data['location'],
            'budget': float(data['budget']),
            'deadline': data['deadline'],
            'status': data['status'],
            'createdAt': data['created_at'],
            'scheduledDate': None,
            'completedDate': None,
            'invitedWorkerId': worker_id
        }
        
        return Response(job_data)
