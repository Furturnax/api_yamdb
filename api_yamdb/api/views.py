from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.views import APIView

from api.filters import TitleFilter
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
    GetTokenSerializer,
    ReviewSerializer,
    SignUpSerializer,
    TitleGetSerializer,
    TitleWriteSerializer,
    UserSerializer
)
from api_yamdb.consts import CANT_USED_IN_USERNAME
from reviews.models import Category, Genre, Review, Title
from users.models import User


class GenreCategoryMixin(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """ViewSet для жанров и категорий."""

    permission_classes = (IsAdminOrReadOnly,)
    search_fields = ('name',)
    lookup_field = 'slug'
    filter_backends = (SearchFilter,)


class GenreViewSet(GenreCategoryMixin):
    """View-класс для жанров."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(GenreCategoryMixin):
    """View-класс для категории."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TitleViewSet(viewsets.ModelViewSet):
    """View-класс для произведения."""

    permission_classes = (IsAdminOrReadOnly,)
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).order_by('rating').all()
    serializer_class = TitleGetSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = TitleFilter
    ordering_fields = ('rating', 'year', 'name')
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_serializer_class(self):
        """Определяет класс сериализатора в зависимости от типа запроса."""
        if self.request.method in SAFE_METHODS:
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
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        """Получает запрос для комментариев автора данного отзыва."""
        return self.get_review().comments.all().select_related('author')

    def perform_create(self, serializer):
        """Создает новый комментарий."""
        serializer.save(author=self.request.user, review=self.get_review())


class UserViewSet(viewsets.ModelViewSet):
    """Управление данными пользователя."""

    queryset = User.objects.all()
    permission_classes = (IsAdmin,)
    serializer_class = AdminUserSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ('get', 'post', 'patch', 'delete')

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated],
        url_path=CANT_USED_IN_USERNAME,
    )
    def get_user_data(self, request):
        """Получение данных пользователя."""
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @get_user_data.mapping.patch
    def update_user_data(self, request):
        """Частичное обновление данных пользователя."""
        serializer = UserSerializer(
            request.user,
            partial=True,
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class APISignup(APIView):
    """Создает нового пользователя."""

    def post(self, request):
        """Обрабатывает POST-запрос для регистрации пользователя."""
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        serializer.create(validated_data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class APIGetToken(APIView):
    """Работа с JWT токеном."""

    def post(self, request):
        """Обрабатывает POST-запрос для генерации токена."""
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        access_token = AccessToken.for_user()
        access_token_data = {'token': str(access_token)}
        return Response(access_token_data, status=status.HTTP_200_OK)
