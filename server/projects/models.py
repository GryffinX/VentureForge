from django.db import models
import uuid
from django.conf import settings

# Create your models here.

User = settings.AUTH_USER_MODEL

class Skill(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"Skill: {self.name}"
    
class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"Category: {self.name}"
    
class Project(models.Model):

    STATUS_CHOICES = [
        ('open','Open'),
        ('in_progress','In Progress'),
        ('completed','Completed'),
        ('cancelled','Cancelled'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    budget_min = models.DecimalField(max_digits=10, decimal_places=2)
    budget_max = models.DecimalField(max_digits=10, decimal_places=2)

    deadline = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Project: {self.title} (Status: {self.status})"
    
class Proposal(models.Model):

    STATUS_CHOICES = [
        ('pending','Pending'),
        ('accepted','Accepted'),
        ('rejected','Rejected'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='proposals')
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='proposals')

    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_days = models.IntegerField()
    cover_letter = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Proposal by {self.freelancer.name} → {self.project.title}"
    

class FreelancerSkill(models.Model):
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='freelancer_skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='freelancer_skills')
    proficiency_level = models.IntegerField(default=1)

    class Meta:
        unique_together = ('freelancer', 'skill')

class ProjectSkill(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='project_skills')

    class Meta:
        unique_together = ('project','skill')

