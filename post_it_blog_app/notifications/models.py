from django.db import models
from django.contrib.auth.models import User


class Notification(models.Model):
    class Type(models.TextChoices):
        LIKE = 'like', 'Like'
        COMMENT = 'comment', 'Comment'
        FOLLOW = 'follow', 'Follow'
        MESSAGE = 'message', 'Message'

    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications')
    notification_type = models.CharField(max_length=20, choices=Type.choices)
    # Generic link to a post (optional — not all notifications relate to a post)
    post = models.ForeignKey(
        'post_it.Post',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='notifications',
    )
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.sender.username} → {self.recipient.username} ({self.notification_type})"
