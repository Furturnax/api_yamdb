from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api_yamdb.consts import LENGTH_150_CHAR, LENGTH_254_CHAR
from reviews.validators import username_validator
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import CustomUser


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class TitleGetSerializer(serializers.ModelSerializer):
    """Сериализатор для получения произведений."""

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category', 'rating'
        )


class TitleWriteSerializer(serializers.ModelSerializer):
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

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')


class AuthorSerializer(serializers.ModelSerializer):
    """Миксин сериализатор поля автора."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        fields = '__all__'


class ReviewSerializer(AuthorSerializer):
    """Сериализатор для отзывов."""

    class Meta(AuthorSerializer.Meta):
        model = Review
        read_only_fields = ('title',)

    def validate(self, data):
        request = self.context.get('request')
        if request.method != 'POST':
            return data
        title = get_object_or_404(
            Title, pk=self.context['view'].kwargs.get('title_id')
        )
        if title.reviews.filter(author=request.user).exists():
            raise ValidationError(
                'Можно оставить только один отзыв на произведение!'
            )
        return data


class CommentSerializer(AuthorSerializer):
    """Сериализатор для произведений."""

    class Meta(AuthorSerializer.Meta):
        model = Comment
        read_only_fields = ('review',)


class AdminUserSerializer(serializers.ModelSerializer):
    """Сериализатор для администратора."""

    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class UserSerializer(AdminUserSerializer):
    """
    Сериализатор для пользователя.
    Возможность редактирования всех полей, кроме роли.
    """

    class Meta(AdminUserSerializer.Meta):
        read_only_fields = ('role',)


class SignUpSerializer(serializers.Serializer):
    """Сериализатор для регистрации пользователя."""

    username = serializers.CharField(
        max_length=LENGTH_150_CHAR,
        required=True,
        validators=[username_validator],
    )
    email = serializers.EmailField(
        max_length=LENGTH_254_CHAR,
        required=True,
    )

    def validate(self, value):
        """Возвращает валидные данные."""
        user_data = CustomUser.objects.filter(
            username=value.get('username'),
            email=value.get('email')
        )
        if not user_data.exists():
            if CustomUser.objects.filter(username=value.get('username')):
                raise ValidationError(
                    'Пользователь с таким username существует.'
                )
            if CustomUser.objects.filter(email=value.get('email')):
                raise ValidationError('Пользователь с таким email существует.')
        return value


class GetTokenSerializer(serializers.Serializer):
    """Сериализатор для получения токена."""

    username = serializers.CharField(
        max_length=LENGTH_150_CHAR,
        required=True,
    )
    confirmation_code = serializers.CharField(
        required=True,
    )
