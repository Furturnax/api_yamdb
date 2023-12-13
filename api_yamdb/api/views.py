from django.conf import settings
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.filters import TitleFilter
from api.mixins import GenreCategoryMixin
from api.permissions import (
    IsAdmin,
    IsAdminModeratorAuthorReadOnly,
    IsAdminOrReadOnly
)
from api.serializers import (
    AdminUserSerializer,
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleGetSerializer,
    TitleWriteSerializer,
    UserSerializer
)
from reviews.models import Category, Genre, Title
from users.models import CustomUser


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
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_serializer_class(self):
        """Определяет класс сериализатора в зависимости от типа запроса."""
        if self.action in ('list', 'retrieve'):
            return TitleGetSerializer
        return TitleWriteSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet для отзывов."""

    permission_classes = (IsAdminModeratorAuthorReadOnly,)
    serializer_class = ReviewSerializer
    http_method_names = ('get', 'post', 'patch', 'delete')

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
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_review(self):
        """Получает отзыв."""
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        """Получает запрос для комментариев автора данного отзыва."""
        return self.get_review().comments.all().select_related('author')

    def perform_create(self, serializer):
        """Создает новый комментарий."""
        serializer.save(author=self.request.user, review=self.get_review())


class UserViewSet(viewsets.ModelViewSet):
    """Управление данными пользователя."""

    queryset = CustomUser.objects.all()
    permission_classes = (IsAdmin,)
    serializer_class = (AdminUserSerializer,)
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    http_method_names = ('get', 'post', 'patch', 'delete')

    @action(
        detail=False,
        methods=('get',),
        permission_classes=(IsAuthenticated,),
        url_path=settings.CANT_USED_IN_USERNAME,
    )
    def user_read(self, request):
        """Чтение данных пользователя."""
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=('patch',),
        permission_classes=(IsAuthenticated,),
        url_path=settings.CANT_USED_IN_USERNAME,
    )
    def user_edit(self, request):
        """Редактирование данных пользователя."""
        serializer = UserSerializer(
            request.user, partial=True, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
