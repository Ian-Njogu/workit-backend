import django_filters
from .models import WorkerProfile

class WorkerProfileFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(lookup_expr='icontains')
    location = django_filters.CharFilter(lookup_expr='icontains')
    available = django_filters.BooleanFilter()
    min_hourly_rate = django_filters.NumberFilter(field_name='hourly_rate', lookup_expr='gte')
    max_hourly_rate = django_filters.NumberFilter(field_name='hourly_rate', lookup_expr='lte')
    min_rating = django_filters.NumberFilter(field_name='rating', lookup_expr='gte')
    
    class Meta:
        model = WorkerProfile
        fields = ['category', 'location', 'available', 'min_hourly_rate', 'max_hourly_rate', 'min_rating']
