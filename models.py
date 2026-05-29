from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """Custom user model for MiniTune."""
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(blank=True)
    channel_name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'channel_name']

    def __str__(self):
        return self.email
