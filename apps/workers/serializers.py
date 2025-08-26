from rest_framework import serializers
from .models import WorkerProfile
from apps.users.serializers import UserPublicSerializer

class WorkerProfileSerializer(serializers.ModelSerializer):
    user = UserPublicSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = WorkerProfile
        fields = [
            'id', 'user', 'user_id', 'category', 'location', 'hourly_rate',
            'rating', 'review_count', 'skills', 'portfolio', 'available'
        ]
        read_only_fields = ['id', 'rating', 'review_count']
    
    def validate_user_id(self, value):
        from apps.users.models import User
        try:
            user = User.objects.get(id=value, role='worker')
            return value
        except User.DoesNotExist:
            raise serializers.ValidationError("User must exist and have worker role")
    
    def create(self, validated_data):
        user_id = validated_data.pop('user_id')
        validated_data['user_id'] = user_id
        return super().create(validated_data)

class WorkerProfileListSerializer(serializers.ModelSerializer):
    user = UserPublicSerializer(read_only=True)
    
    class Meta:
        model = WorkerProfile
        fields = [
            'id', 'user', 'category', 'location', 'hourly_rate',
            'rating', 'review_count', 'available'
        ]
