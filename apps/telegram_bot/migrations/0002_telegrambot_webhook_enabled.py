# Generated by Django 5.0.1 on 2024-02-08 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telegram_bot', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegrambot',
            name='webhook_enabled',
            field=models.BooleanField(default=False),
        ),
    ]