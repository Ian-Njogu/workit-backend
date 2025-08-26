from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import WorkerProfile
from .serializers import WorkerProfileSerializer, WorkerProfileListSerializer
from .filters import WorkerProfileFilter

class WorkersViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing worker profiles.
    Supports filtering by category, location, and other criteria.
    """
    queryset = WorkerProfile.objects.select_related('user').filter(available=True)
    serializer_class = WorkerProfileListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = WorkerProfileFilter
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return WorkerProfileSerializer
        return WorkerProfileListSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Apply additional filters
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__icontains=category)
        
        location = self.request.query_params.get('location')
        if location:
            queryset = queryset.filter(location__icontains=location)
        
        return queryset.order_by('-rating', '-review_count')
