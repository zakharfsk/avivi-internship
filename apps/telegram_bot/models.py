import requests
from django.db import models


class TelegramBot(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    token = models.CharField(max_length=255)
    webhook_enabled = models.BooleanField(default=False)

    def set_webhook(self, url: str):
        response = requests.get(
            f'https://api.telegram.org/bot{self.token}/setWebhook',
            params={'url': url}
        )
        return response.json()

    def delete_webhook(self):
        response = requests.get(f'https://api.telegram.org/bot{self.token}/deleteWebhook')
        return response.json()

    def __str__(self):
        return self.name + ' ' + self.username
