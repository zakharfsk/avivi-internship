from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.username


class TelegramUser(models.Model):
    telegram_id = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=255, unique=True, blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True)
    state_data = models.JSONField(blank=True, null=True)
    two_auth_enabled = models.BooleanField(default=False)
    lang = models.CharField(max_length=5, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username
