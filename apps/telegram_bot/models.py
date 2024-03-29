from django.db import models


class TelegramBot(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    token = models.CharField(max_length=255)
    webhook_enabled = models.BooleanField(default=False)

    def __str__(self):
        return self.name + ' ' + self.username
