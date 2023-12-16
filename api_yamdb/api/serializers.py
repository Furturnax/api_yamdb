from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api_yamdb.consts import LENGTH_EMAIL, LENGTH_USERNAME
from reviews.models import Category, Comment, Genre, Review, Title
from reviews.validators import username_validator
from users.models import User


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

    def to_representation(self, instance):
        """Переопределение to_representation для изменения вывода данных."""
        title_get_serializer = TitleGetSerializer(instance)
        return title_get_serializer.data

    def validate_genre(self, value):
        """Проверка валидности списка жанров."""
        if not value:
            raise ValidationError('Жанр обязателен.')
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """Миксин сериализатор поля автора."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )


class ReviewSerializer(AuthorSerializer):
    """Сериализатор для отзывов."""

    class Meta():
        model = Review
        fields = ('id', 'title', 'score', 'author', 'text', 'pub_date')
        read_only_fields = ('title',)

    def validate(self, data):
        """Проверяет, что пользователь может оставить только один отзыв."""
        request = self.context.get('request')
        if request.method != 'POST':
            return data
        title_id = self.context['view'].kwargs.get('title_id')
        if Review.objects.filter(
            title_id=title_id,
            author=request.user
        ).exists():
            raise ValidationError(
                'Можно оставить только один отзыв на произведение.'
            )
        return data


class CommentSerializer(AuthorSerializer):
    """Сериализатор для произведений."""

    class Meta:
        model = Comment
        fields = ('id', 'review', 'author', 'text', 'pub_date')
        read_only_fields = ('review',)


class AdminUserSerializer(serializers.ModelSerializer):
    """Сериализатор для администратора."""

    class Meta:
        model = User
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
        max_length=LENGTH_USERNAME,
        required=True,
        validators=(username_validator,),
    )
    email = serializers.EmailField(
        max_length=LENGTH_EMAIL,
        required=True,
    )

    def validate(self, value):
        """Возвращает валидные данные."""
        user_data = User.objects.filter(
            username=value.get('username'),
            email=value.get('email')
        )
        if user_data.exists():
            return value
        if User.objects.filter(username=value.get('username')):
            raise ValidationError(
                'Пользователь с таким username существует.'
            )
        if User.objects.filter(email=value.get('email')):
            raise ValidationError(
                'Пользователь с таким email существует.'
            )
        return value

    def create(self, validated_data):
        """Создает пользователя и отправляет письмо с confirmation code."""
        user, created = User.objects.get_or_create(**validated_data)
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Регистрация на сайте YaMDb',
            message=f'Код для подтверждения регистрации: {confirmation_code}',
            from_email=settings.FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=True,
        )
        return user


class GetTokenSerializer(serializers.Serializer):
    """Сериализатор для получения токена."""

    username = serializers.CharField(
        max_length=LENGTH_USERNAME,
        required=True,
    )
    confirmation_code = serializers.CharField(
        required=True,
    )

    def validate(self, data):
        """Валидирует данные пользователя для JWT токена."""
        username, confirmation_code = data.values()
        user = get_object_or_404(User, username=username)
        if not default_token_generator.check_token(
            user, confirmation_code
        ):
            raise ValidationError(
                {'confirmation_code': 'Код подтверждения неверный'}
            )
        user.is_active = True
        user.save()
        return data
