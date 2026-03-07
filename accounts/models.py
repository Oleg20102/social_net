from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class OnlineStatus(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="online_status"
    )
    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} — {'online' if self.is_online else 'offline'}"

class User(AbstractUser):
    avatar = models.ImageField(
        upload_to='avatars/',
        default='avatars/default.png',
        blank=True
    )
    bio = models.TextField(blank=True, max_length=300)

    def __str__(self):
        return self.username
