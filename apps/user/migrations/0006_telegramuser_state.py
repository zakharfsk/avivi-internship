# Generated by Django 5.0.1 on 2024-02-19 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_alter_telegramuser_first_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegramuser',
            name='state',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]