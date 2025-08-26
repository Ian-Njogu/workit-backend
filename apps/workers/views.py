from rest_framework import viewsets, permissions, status
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
    
    @action(detail=False, methods=['get'], url_path='categories')
    def categories(self, request):
        """
        Get all categories (matches mock API /api/v1/categories).
        """
        categories = [
            { 'id': 1, 'name': 'Plumbing', 'icon': '🔧' },
            { 'id': 2, 'name': 'Cleaning', 'icon': '🧹' },
            { 'id': 3, 'name': 'Electrical', 'icon': '⚡' },
            { 'id': 4, 'name': 'Carpentry', 'icon': '🔨' },
            { 'id': 5, 'name': 'Painting', 'icon': '🎨' },
            { 'id': 6, 'name': 'Gardening', 'icon': '🌱' },
            { 'id': 7, 'name': 'Moving', 'icon': '📦' },
            { 'id': 8, 'name': 'General Labor', 'icon': '👷' }
        ]
        return Response(categories)
    
    def list(self, request, *args, **kwargs):
        """
        Override list to match mock API response format exactly.
        """
        queryset = self.filter_queryset(self.get_queryset())
        
        # Get pagination parameters
        page = int(request.query_params.get('page', 1))
        limit = int(request.query_params.get('limit', 10))
        
        # Manual pagination to match mock format
        start = (page - 1) * limit
        end = start + limit
        paginated_queryset = queryset[start:end]
        
        # Serialize with mock-compatible format
        serializer = self.get_serializer(paginated_queryset, many=True)
        
        # Transform to match mock API response structure
        workers_data = []
        for item in serializer.data:
            worker_data = {
                'id': item['id'],
                'name': item['user']['name'],
                'category': item['category'],
                'categoryId': item.get('category_id', 1),  # Mock has categoryId
                'location': item['location'],
                'hourlyRate': float(item['hourly_rate']),  # Mock has hourlyRate
                'rating': float(item['rating']),
                'reviewCount': item['review_count'],  # Mock has reviewCount
                'skills': item.get('skills', []),
                'experience': '3 years',  # Mock has experience field
                'available': item['available'],
                'portfolio': item.get('portfolio', []),
                'reviews': []  # Mock has reviews array
            }
            workers_data.append(worker_data)
        
        return Response({
            'workers': workers_data,
            'pagination': {
                'page': page,
                'limit': limit,
                'total': queryset.count(),
                'totalPages': (queryset.count() + limit - 1) // limit
            }
        })
    
    def retrieve(self, request, *args, **kwargs):
        """
        Override retrieve to match mock API response format exactly.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        
        # Transform to match mock API response structure
        worker_data = {
            'id': data['id'],
            'name': data['user']['name'],
            'category': data['category'],
            'categoryId': 1,  # Mock has categoryId
            'location': data['location'],
            'hourlyRate': float(data['hourly_rate']),
            'rating': float(data['rating']),
            'reviewCount': data['review_count'],
            'skills': data.get('skills', []),
            'experience': '3 years',
            'available': data['available'],
            'portfolio': data.get('portfolio', []),
            'reviews': []
        }
        
        return Response(worker_data)
