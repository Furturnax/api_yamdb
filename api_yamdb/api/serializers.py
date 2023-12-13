from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.mixins import AuthorSerializer
from reviews.models import Category, Comment, Genre, Review, Title


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров."""

    class Meta:
        model = Genre
        fields = ('name', 'slug',)


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""

    class Meta:
        model = Category
        fields = ('name', 'slug',)


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для произведений."""

    class Meta:
        model = Title
        fields = '__all__'


class TitleGetSerializer(TitleSerializer):
    """Сериализатор для получения произведений."""

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(read_only=True)


class TitleWriteSerializer(TitleSerializer):
    """Сериализатор для изменения произведений."""

    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )


class ReviewSerializer(AuthorSerializer):
    """Сериализатор для отзывов."""

    class Meta:
        model = Review
        read_only_fields = ('title',)

    def validate(self, data):
        """Валидация на POST-запрос."""
        if self.context.get('request').method != 'POST':
            return data
        return self.validate_unique_review(data.get('title'))

    def validate_unique_review(self, value):
        """Дополнительная валидация для одного отзыва на автора."""
        title = get_object_or_404(
            Title, pk=self.context['view'].kwargs.get('title_id')
        )
        request = self.context.get('request')
        if title.objects.filter(author=request.user).exists():
            raise ValidationError('Можно оставить только один отзыв.')
        return value


class CommentSerializer(AuthorSerializer):
    """Сериализатор для произведений."""

    class Meta(AuthorSerializer.Meta):
        model = Comment
        read_only_fields = ('review',)
