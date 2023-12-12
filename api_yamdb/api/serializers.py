from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import CustomUser


class AuthorSerializer(serializers.ModelSerializer):
    """Базовый сериализатор поля author."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        fields = '__all__'


class ReviewSerializer(AuthorSerializer):
    """Сериализатор для отзывов."""

#TODO
    class Meta(AuthorSerializer.Meta):
        model = Review
        read_only_fields = ('title',)


class CommentSerializer(AuthorSerializer):
    """Сериализатор для произведений."""

    class Meta(AuthorSerializer.Meta):
        model = Comment
        read_only_fields = ('review',)


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""

    class Meta:
        model = Category
        fields = ('name', 'slug',)


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров."""

    class Meta:
        model = Genre
        fields = ('name', 'slug',)


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для произведений."""

    class Meta:
        model = Title
        fields = '__all__'


class TitleGetSerializer(serializers.ModelSerializer):
    """Сериализатор для получения произведений."""


class TitleWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для изменения произведений."""

