from django.db import models
#from django.contrib.auth.models import User

# Create your models here.

# class Conversation(models.Model):
#     title = models.CharField(max_length=100, unique=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)

#     def __str__(self):
#         return f"{self.user.username}: {self.title}"
    
# class ChatMessage(models.Model):
#     conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
#     user_response = models.TextField(null=True, blank=True)
#     ai_response = models.TextField(null=True, blank=True)
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Message {self.id} in {self.conversation.title}"