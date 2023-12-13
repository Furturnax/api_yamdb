from rest_framework import mixins, viewsets
from rest_framework import serializers

from api.permissions import IsAdminOrReadOnly


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


class AuthorSerializer(serializers.ModelSerializer):
    """Миксин сериализатор поля автора."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        fields = '__all__'
