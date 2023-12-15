from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from reviews.models import CustomUser


@admin.register(CustomUser)
class UserAdmin(BaseUserAdmin):
    """Интерфейс управления пользователями."""

    list_display = (
        'id', 'username', 'email', 'first_name', 'last_name', 'role'
    )
    list_filter = ('role',)
    search_fields = ('username', 'email')
    ordering = ('-id',)
    list_editable = ('role',)
