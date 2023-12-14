from django.contrib import admin

from reviews.models import Title, Category, Genre, Review, Comment, CustomUser


@admin.register(Title, Category, Genre, Review, Comment)
class ReviewsAdmin(admin.ModelAdmin):
    pass


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    """Интерфейс управления пользователями."""

    list_display = (
        'pk',
        'username',
        'email',
        'first_name',
        'last_name',
        'role',
    )
    search_fields = (
        'username',
        'email',
    )
    list_editable = ('role',)
    list_filter = ('role',)
