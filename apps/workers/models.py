from django.db import models
from django.conf import settings

class WorkerProfile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="worker_profile")
	category = models.CharField(max_length=120)
	location = models.CharField(max_length=120)
	hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
	rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
	review_count = models.IntegerField(default=0)
	skills = models.JSONField(default=list, blank=True)
	portfolio = models.JSONField(default=list, blank=True)
	available = models.BooleanField(default=True)

	def __str__(self) -> str:
		return f"WorkerProfile<{self.user_id}>"
