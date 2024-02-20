from django.contrib import admin

from .models import Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'created_at')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'description')
    list_filter = ('created_at',)
    list_per_page = 20
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('user', 'title', 'description')
        }),
        ('Date information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    ordering = ('-created_at',)
