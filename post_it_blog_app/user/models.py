from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, default='avatars/default.png')
    bio = models.TextField(blank=True)
    display_name = models.CharField(max_length=100, blank=True)

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

    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return static('user/images/default_avatar.png')

    @property
    def name_or_username(self):
        return (
            self.display_name
            or self.user.get_full_name()
            or self.user.username
        )