# Generated by Django 5.0.1 on 2024-02-20 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_alter_telegramuser_first_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegramuser',
            name='state_data',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
