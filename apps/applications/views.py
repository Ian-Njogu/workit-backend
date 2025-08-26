from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Application
from .serializers import ApplicationSerializer

class ApplicationsViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = Application.objects.select_related("job", "worker").all()
	serializer_class = ApplicationSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		qs = super().get_queryset()
		client_id = self.request.query_params.get("client_id")
		job_id = self.request.query_params.get("job_id")
		if client_id:
			qs = qs.filter(job__client_id=client_id)
		if job_id:
			qs = qs.filter(job_id=job_id)
		return qs

	@action(detail=True, methods=["post"], url_path="accept", permission_classes=[permissions.IsAuthenticated])
	def accept(self, request, pk=None):
		return Response(status=status.HTTP_200_OK)

	@action(detail=True, methods=["post"], url_path="reject", permission_classes=[permissions.IsAuthenticated])
	def reject(self, request, pk=None):
		return Response(status=status.HTTP_200_OK)
