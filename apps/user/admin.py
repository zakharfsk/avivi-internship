from django.contrib import admin

from .models import User, TelegramUser


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "first_name",
        "last_name",
        "email",
        "is_staff",
        "is_active",
        "date_joined",
    )
    list_display_links = ("username", "id",)
    list_filter = ("is_staff", "is_active")
    search_fields = ("username", "first_name", "last_name", "email")
    filter_horizontal = ("groups", "user_permissions",)
    ordering = ("username",)
    readonly_fields = ("date_joined", "password")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "password",
                )
            },
        ),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "phone_number",
                    "birth_date",
                    "bio",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions"
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "telegram_id",
        "username",
        "first_name",
        "last_name",
        "date_created",
        "date_updated",
    )
    list_display_links = ("id", "telegram_id")
    search_fields = ("telegram_id", "username", )
    ordering = ("username",)
    readonly_fields = ("date_created", "date_updated", "telegram_id")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "telegram_id",
                    "username",
                    "first_name",
                    "last_name",
                )
            },
        ),
        ("Important dates", {"fields": ("date_created", "date_updated")}),
    )
