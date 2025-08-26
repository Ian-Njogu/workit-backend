from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
	use_in_migrations = True

	def _create_user(self, email: str, password: str | None, **extra_fields):
		if not email:
			raise ValueError("The email must be set")
		email = self.normalize_email(email)
		user = self.model(email=email, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, email: str, password: str | None = None, **extra_fields):
		extra_fields.setdefault("is_staff", False)
		extra_fields.setdefault("is_superuser", False)
		return self._create_user(email, password, **extra_fields)

	def create_superuser(self, email: str, password: str | None, **extra_fields):
		extra_fields.setdefault("is_staff", True)
		extra_fields.setdefault("is_superuser", True)
		if extra_fields.get("is_staff") is not True:
			raise ValueError("Superuser must have is_staff=True.")
		if extra_fields.get("is_superuser") is not True:
			raise ValueError("Superuser must have is_superuser=True.")
		# Provide defaults for required fields if not supplied
		extra_fields.setdefault("name", "Admin")
		extra_fields.setdefault("role", "client")
		return self._create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
	ROLE_CLIENT = "client"
	ROLE_WORKER = "worker"
	ROLE_CHOICES = [
		(ROLE_CLIENT, "Client"),
		(ROLE_WORKER, "Worker"),
	]

	email = models.EmailField(unique=True)
	name = models.CharField(max_length=255)
	role = models.CharField(max_length=20, choices=ROLE_CHOICES)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)

	USERNAME_FIELD = "email"
	REQUIRED_FIELDS = ["name", "role"]

	objects = UserManager()

	def __str__(self) -> str:
		return f"{self.email} ({self.role})"
