from rest_framework import serializers
from .models import Job
from apps.users.serializers import UserPublicSerializer

class JobSerializer(serializers.ModelSerializer):
    client = UserPublicSerializer(read_only=True)
    worker = UserPublicSerializer(read_only=True)
    
    class Meta:
        model = Job
        fields = [
            'id', 'client', 'worker', 'title', 'category', 'description',
            'location', 'budget', 'deadline', 'status', 'created_at'
        ]
        read_only_fields = ['id', 'client', 'worker', 'created_at']
    
    def validate_status(self, value):
        if self.instance:
            # Check status transitions
            current_status = self.instance.status
            allowed_transitions = {
                'pending': ['accepted', 'cancelled'],
                'accepted': ['in_progress', 'cancelled'],
                'in_progress': ['completed', 'cancelled'],
                'completed': [],
                'cancelled': []
            }
            if value != current_status and value not in allowed_transitions.get(current_status, []):
                raise serializers.ValidationError(
                    f"Invalid status transition from {current_status} to {value}"
                )
        return value

class JobCreateSerializer(serializers.ModelSerializer):
    invited_worker_id = serializers.IntegerField(required=False, allow_null=True)
    
    class Meta:
        model = Job
        fields = [
            'title', 'category', 'description', 'location', 'budget',
            'deadline', 'invited_worker_id'
        ]
    
    def validate_invited_worker_id(self, value):
        if value:
            from apps.users.models import User
            try:
                user = User.objects.get(id=value, role='worker')
                return value
            except User.DoesNotExist:
                raise serializers.ValidationError("Invited worker must exist and have worker role")
        return value

class JobFeedSerializer(serializers.ModelSerializer):
    client = UserPublicSerializer(read_only=True)
    
    class Meta:
        model = Job
        fields = [
            'id', 'client', 'title', 'category', 'description',
            'location', 'budget', 'deadline', 'status', 'created_at'
        ]
