from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, name, role, password=None):
        if not email:
            raise ValueError('The email field must be set')
        email = self.normalize_email(email)

        user = self.model(
            email=email,
            name=name,
            role=role
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, name, role='admin', password=None):
        user = self.create_user(email,name,role,password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Users(AbstractBaseUser, PermissionsMixin):

    ROLES = [
        ('freelancer', 'Freelancer'),
        ('client', 'Client'),
        ('admin', 'Admin'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, null=False)
    role = models.CharField(max_length=20, choices=ROLES)
    wallet_address = models.CharField(max_length=255, unique=True, null=True, blank=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)   

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'role']

    def __str__(self):
        return f"{self.name} ({self.role})"

from django.conf import settings

User = settings.AUTH_USER_MODEL

class Freelancer(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='freelancer_profile')
    bio = models.TextField(blank=True)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    experience = models.IntegerField(null=True, blank=True)
    avg_rating = models.DecimalField(max_digits=3, decimal_places=2, null=False, default=0.00)
    projects_complete = models.IntegerField(default=0, null=False)
    response_time = models.IntegerField(default=24)

    def __str__(self):
        return f"Freelancer: {self.user.name} ({self.user.email})"
    
class Client(models.Model):
        id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
        user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client_profile')
        company_name = models.CharField(max_length=255, blank=True, null=True)
        total_spent = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
        total_projects_posted = models.IntegerField(default=0)

        def __str__(self):
            return f"Client: {self.user.name} ({self.user.email})"

