from django.db import models
import uuid
from django.conf import settings
from contracts.models import Milestone, Contract

# Create your models here.

User = settings.AUTH_USER_MODEL

class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending','Pending'),
        ('completed','Completed'),
        ('failed','Failed'),
        ('refunded','Refunded'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='payments')
    milestone = models.ForeignKey(Milestone, on_delete=models.CASCADE, related_name='payments')
 
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=30)
    transaction_hash = models.CharField(max_length=255, unique=True, blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment of {self.amount} for Milestone: {self.milestone.title} (Status: {self.status})"
    
