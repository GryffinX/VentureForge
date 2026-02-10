from django.db import models
import uuid
from django.conf import settings

# Create your models here.

User = settings.AUTH_USER_MODEL

class Notification(models.Model):
    TYPE_CHOICES = [
        ('proposal','Proposal'),
        ('message','Message'),
        ('milestone','Milestone'),
        ('payment','Payment'),
        ('dispute','Dispute'),
         ('review','Review'),  
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")

    title = models.CharField(max_length=255)
    message = models.TextField()

    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.title}"
    