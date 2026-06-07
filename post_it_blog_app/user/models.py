from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True)
    # Followers: a user can follow many users, and be followed by many users
    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers',
        blank=True,
    )

    def __str__(self):
        return f"Profile of {self.user.username}"

    @property
    def follower_count(self):
        return self.followers.count()

    @property
    def following_count(self):
        return self.following.count()
