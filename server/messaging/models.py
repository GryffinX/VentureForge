from django.db import models
import uuid
from django.conf import settings

# Create your models here.


User = settings.AUTH_USER_MODEL

class Conversation(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_conversations')
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='freelancer_conversations')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation between {self.client.name} and {self.freelancer.name} | Conversation ID: {self.id}"
    
class ChatMessage(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')

    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender.name} at {self.timestamp} | Read: {self.is_read}"