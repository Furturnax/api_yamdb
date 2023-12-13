from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter

from api.filters import TitleFilter
from api.mixins import GenreCategoryMixin
from api.permissions import IsAdminModeratorAuthorReadOnly, IsAdminOrReadOnly
from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleGetSerializer,
    TitleWriteSerializer
)
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

    
class TitleViewSet(viewsets.ModelViewSet):
    """View-класс для произведения."""

    permission_classes = (IsAdminOrReadOnly,)
    queryset = Title.objects.annotate(rating=Avg('reviews__score')).all()
    serializer_class = TitleGetSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = TitleFilter

    def get_serializer_class(self):
        """Определяет класс сериализатора в зависимости от типа запроса."""
        if self.action in ('list', 'retrieve'):
            return TitleGetSerializer
        return TitleWriteSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet для отзывов."""

    permission_classes = (IsAdminModeratorAuthorReadOnly,)
    serializer_class = ReviewSerializer

    def get_title(self):
        """Получает произведение."""
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        """Получает запрос для всех отзывов данного произведения."""
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        """Создает новый отзыв."""
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для комментариев."""

    permission_classes = (IsAdminModeratorAuthorReadOnly,)
    serializer_class = CommentSerializer

    def get_review(self):
        """Получает отзыв."""
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        """Получает запрос для комментариев автора данного отзыва."""
        return self.get_review().comments.all().select_related('author')

    def perform_create(self, serializer):
        """Создает новый комментарий."""
        serializer.save(author=self.request.user, review=self.get_review())
