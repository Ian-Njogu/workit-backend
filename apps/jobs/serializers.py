from rest_framework import serializers
from .models import Job
from apps.users.serializers import UserPublicSerializer

class JobSerializer(serializers.ModelSerializer):
	client = UserPublicSerializer(read_only=True)
	worker = UserPublicSerializer(read_only=True)

	class Meta:
		model = Job
		fields = [
			"id", "client", "worker", "title", "category", "description",
			"location", "budget", "deadline", "status", "created_at"
		]

class JobCreateSerializer(serializers.ModelSerializer):
	invited_worker_id = serializers.IntegerField(required=False, write_only=True)

	class Meta:
		model = Job
		fields = ["title", "category", "description", "location", "budget", "deadline", "invited_worker_id"]
