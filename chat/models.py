from django.contrib.auth.models import User
from django.db import models

# این مدل هر گفتگوی کامل بین کاربر و ربات را نگه می‌دارد
class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation with {self.user.username}"

# این مدل هر پیام تکی (چه از طرف کاربر و چه ربات) را ذخیره می‌کند
class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    text = models.TextField()
    is_from_user = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{'User' if self.is_from_user else 'Bot'}: {self.text[:30]}..."