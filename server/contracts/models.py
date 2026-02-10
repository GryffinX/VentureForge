from django.db import models
import uuid
from django.conf import settings
from projects.models import Project

# Create your models here.

User = settings.AUTH_USER_MODEL

class Contract(models.Model):

    STATUS_CHOICES = [
        ('active','Active'),
        ('completed','Completed'),
        ('cancelled','Cancelled'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='contracts')
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_contracts')
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='freelancer_contracts')

    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    def __str__(self):
        return f'Contract for Project: {self.project.title} (Status: {self.status})'
    
class Milestone(models.Model):
    STATUS_CHOICES = [
        ('pending','Pending'),
        ('completed','Completed'),
        ('approved','Approved'),
        ('rejected','Rejected'),
        ('disputed','Disputed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='milestones')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    escrow_tx_hash = models.CharField(max_length=255, unique=True, null=True, blank=True, default=None)
    escrow_status = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return f"Milestone: {self.title} (Status: {self.status})"

class Deliverable(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    milestone = models.ForeignKey(Milestone, on_delete=models.CASCADE, related_name='deliverables')

    file_url = models.URLField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Deliverable for Milestone: {self.milestone.title} (Approved: {self.approved})"
    

class Dispute(models.Model):

    STATUS_CHOICES = [
        ('open','Open'),
        ('under_review','Under Review'),
        ('resolved', 'Resolved'),
        ('rejected','Rejected'),
    ]

    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='disputes')
    milestone = models.ForeignKey(Milestone, on_delete=models.CASCADE, related_name='disputes')
    raised_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='raised_dispute')
    
    reason = models.TextField(blank=False)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    resolution = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)   

    def __str__(self):
        return f"Dispute for Contract: {self.contract.id} (Status: {self.status})"


