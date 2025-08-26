from rest_framework import serializers
from .models import Application

class ApplicationSerializer(serializers.ModelSerializer):
	worker_name = serializers.CharField(source="worker.name", read_only=True)
	job_title = serializers.CharField(source="job.title", read_only=True)
	job_category = serializers.CharField(source="job.category", read_only=True)
	job_location = serializers.CharField(source="job.location", read_only=True)

	class Meta:
		model = Application
		fields = [
			"id", "job", "worker", "message", "quote", "status", "created_at",
			"worker_name", "job_title", "job_category", "job_location"
		]
		read_only_fields = ["status", "created_at"]
