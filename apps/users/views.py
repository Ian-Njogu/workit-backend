from rest_framework import permissions, views, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import UserPublicSerializer

class LoginView(views.APIView):
	permission_classes = [permissions.AllowAny]

	def post(self, request):
		email = request.data.get("email")
		password = request.data.get("password")
		user = authenticate(request, email=email, password=password)
		if not user:
			return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
		refresh = RefreshToken.for_user(user)
		return Response({
			"access": str(refresh.access_token),
			"refresh": str(refresh),
			"user": UserPublicSerializer(user).data
		})
