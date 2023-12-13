from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleGetSerializer,
    TitleWriteSerializer
)
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from api.mixins import GenreCategoryMixin
from .filters import TitleFilter
from .permissions import IsAdminOrReadOnly
from reviews.models import Category, Genre, Title


class GenreViewSet(GenreCategoryMixin):
    """View-класс для жанров."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (SearchFilter,)


class CategoryViewSet(GenreCategoryMixin):
    """View-класс для категории."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (SearchFilter,)


class TitleViewSet(GenreCategoryMixin):
    """View-класс для категории."""

    queryset = Title.objects.annotate(rating=Avg('reviews__score')).all()
    serializer_class = TitleGetSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filter_class = TitleFilter

    def get_serializer_class(self):
        """Определяет класс сериализатора в зависимости от типа запроса."""
        if self.action in ['list', 'retrieve']:
            return TitleGetSerializer
        return TitleWriteSerializer
