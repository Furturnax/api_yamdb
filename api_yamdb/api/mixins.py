from rest_framework import mixins, viewsets
from rest_framework import serializers

from api.permissions import IsAdminOrReadOnly
from reviews.models import Title
from users.models import CustomUser


class GenreCategoryMixin(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Миксин для жанров и категорий."""

    permission_classes = (IsAdminOrReadOnly,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для произведений."""

    class Meta:
        model = Title
        fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):
    """Миксин сериализатор поля автора."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        fields = '__all__'


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
