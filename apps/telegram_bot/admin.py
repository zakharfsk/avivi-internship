from django.contrib import admin

from .models import TelegramBot


@admin.register(TelegramBot)
class TelegramBotAdmin(admin.ModelAdmin):
    list_display = ('name', 'username', 'token', 'webhook_enabled')
    search_fields = ('name', 'username')
    list_filter = ('name', 'username')
    fields = ('name', 'username', 'token')
