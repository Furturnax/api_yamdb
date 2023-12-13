from api.serializers import CategorySerializer, GenreSerializer
from api.mixins import GenreCategoryMixin
from reviews.models import Category, Genre
from rest_framework.filters import SearchFilter


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
