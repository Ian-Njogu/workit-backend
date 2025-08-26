from rest_framework import serializers
from .models import Application
from apps.users.serializers import UserPublicSerializer
from apps.jobs.serializers import JobFeedSerializer

class ApplicationSerializer(serializers.ModelSerializer):
    worker = UserPublicSerializer(read_only=True)
    job = JobFeedSerializer(read_only=True)
    
    class Meta:
        model = Application
        fields = [
            'id', 'job', 'worker', 'message', 'quote', 'status', 'created_at'
        ]
        read_only_fields = ['id', 'worker', 'status', 'created_at']

class ApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['message', 'quote']
    
    def validate(self, data):
        # Check if worker already applied to this job
        job_id = self.context.get('job_id')
        worker = self.context.get('request').user
        
        if Application.objects.filter(job_id=job_id, worker=worker).exists():
            raise serializers.ValidationError("You have already applied to this job")
        
        return data

class ApplicationListSerializer(serializers.ModelSerializer):
    worker = UserPublicSerializer(read_only=True)
    job = JobFeedSerializer(read_only=True)
    worker_name = serializers.CharField(source='worker.name', read_only=True)
    job_title = serializers.CharField(source='job.title', read_only=True)
    job_category = serializers.CharField(source='job.category', read_only=True)
    job_location = serializers.CharField(source='job.location', read_only=True)
    
    class Meta:
        model = Application
        fields = [
            'id', 'worker', 'job', 'message', 'quote', 'status', 'created_at',
            'worker_name', 'job_title', 'job_category', 'job_location'
        ]
