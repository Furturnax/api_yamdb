from django.contrib import admin
from django.contrib.auth.models import Group

from reviews.models import Title, Category, Genre, Review, Comment

admin.site.unregister(Group)


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Настройка раздела Title."""

    list_display = (
        'name', 'year', 'description', 'category', 'display_genres'
    )
    list_filter = ('category', 'year')
    search_fields = ('category', 'name', 'description')
    ordering = ('category',)
    list_display_links = ('name',)
    filter_horizontal = ('genre',)

    @admin.display(description='Жанры')
    def display_genres(self, obj):
        return ', '.join(genre.name for genre in obj.genre.all())


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Настройка раздела Category."""

    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')
    ordering = ('name',)
    list_display_links = ('name',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Настройка раздела Genre."""

    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')
    ordering = ('name',)
    list_display_links = ('name',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Настройка раздела Review."""

    list_display = ('title', 'text', 'score', 'author', 'pub_date')
    list_filter = ('score', 'author')
    search_fields = ('title', 'text', 'score', 'author')
    ordering = ('-pub_date',)
    list_display_links = ('title',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Настройка раздела Comment."""

    list_display = ('review', 'text', 'author', 'pub_date')
    list_filter = ('review', 'author')
    search_fields = ('review', 'text', 'author')
    ordering = ('-pub_date',)
    list_display_links = ('review',)
