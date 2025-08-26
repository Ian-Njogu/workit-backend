from django.db import models
from django.conf import settings

class Job(models.Model):
	STATUS_PENDING = "pending"
	STATUS_ACCEPTED = "accepted"
	STATUS_IN_PROGRESS = "in_progress"
	STATUS_COMPLETED = "completed"
	STATUS_CANCELLED = "cancelled"
	STATUS_CHOICES = [
		(STATUS_PENDING, "Pending"),
		(STATUS_ACCEPTED, "Accepted"),
		(STATUS_IN_PROGRESS, "In Progress"),
		(STATUS_COMPLETED, "Completed"),
		(STATUS_CANCELLED, "Cancelled"),
	]

	client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="client_jobs")
	worker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="worker_jobs")
	title = models.CharField(max_length=255)
	category = models.CharField(max_length=120)
	description = models.TextField()
	location = models.CharField(max_length=120)
	budget = models.DecimalField(max_digits=12, decimal_places=2)
	deadline = models.DateField(null=True, blank=True)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self) -> str:
		return f"Job<{self.id}> {self.title}"
