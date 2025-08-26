from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Job
from .serializers import JobSerializer, JobCreateSerializer

class JobsViewSet(viewsets.ModelViewSet):
	queryset = Job.objects.select_related("client", "worker").all()
	permission_classes = [permissions.IsAuthenticated]

	def get_serializer_class(self):
		if self.action == "create":
			return JobCreateSerializer
		return JobSerializer

	def perform_create(self, serializer):
		serializer.save(client=self.request.user)

	def get_queryset(self):
		qs = super().get_queryset()
		client_id = self.request.query_params.get("client_id")
		worker_id = self.request.query_params.get("worker_id")
		assigned = self.request.query_params.get("assigned")
		if client_id:
			qs = qs.filter(client_id=client_id)
		if worker_id and assigned == "true":
			qs = qs.filter(worker_id=worker_id)
		return qs

	@action(detail=False, methods=["get"], url_path="feed", permission_classes=[permissions.IsAuthenticated])
	def feed(self, request):
		qs = Job.objects.filter(status=Job.STATUS_PENDING)
		page = self.paginate_queryset(qs)
		if page is not None:
			return self.get_paginated_response(JobSerializer(page, many=True).data)
		return Response(JobSerializer(qs, many=True).data)

	@action(detail=True, methods=["post"], url_path="applications", permission_classes=[permissions.IsAuthenticated])
	def create_application(self, request, pk=None):
		# TODO: implement in ApplicationsViewSet or here via serializer
		return Response(status=status.HTTP_201_CREATED)
