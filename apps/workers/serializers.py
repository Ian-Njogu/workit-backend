from rest_framework import serializers
from .models import WorkerProfile
from apps.users.serializers import UserPublicSerializer

class WorkerProfileSerializer(serializers.ModelSerializer):
	user = UserPublicSerializer(read_only=True)

	class Meta:
		model = WorkerProfile
		fields = [
			"id", "user", "category", "location", "hourly_rate",
			"rating", "review_count", "skills", "portfolio", "available"
		]
