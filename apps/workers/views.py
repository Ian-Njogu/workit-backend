from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import WorkerProfile
from .serializers import WorkerProfileSerializer

class WorkersViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = WorkerProfile.objects.select_related("user").all()
	serializer_class = WorkerProfileSerializer
	permission_classes = [permissions.AllowAny]
	filter_backends = [DjangoFilterBackend, filters.SearchFilter]
	filterset_fields = ["category", "location"]
	search_fields = ["user__name", "category", "location"]
