from django.shortcuts import get_object_or_404
from reviews.models import Category, Genre, Title
from rest_framework import viewsets
from rest_framework.filters import SearchFilter

from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer
)
from api.mixins import GenreCategoryMixin
from api.permissions import IsAdminModeratorAuthorReadOnly


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
