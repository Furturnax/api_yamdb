from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

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
    GetTokenSerializer,
    ReviewSerializer,
    SignUpSerializer,
    TitleGetSerializer,
    TitleWriteSerializer,
    UserSerializer
)
from api_yamdb.consts import CANT_USED_IN_USERNAME
from reviews.models import Category, Genre, Review, Title
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
    filterset_class = TitleFilter
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
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))

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
    serializer_class = AdminUserSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ('get', 'post', 'patch', 'delete')

    @action(
        detail=False,
        methods=('get', 'patch'),
        permission_classes=(IsAuthenticated,),
        url_path=CANT_USED_IN_USERNAME,
    )
    def user_data_operations(self, request):
        """
        GET: Получение данных пользователя.
        PATCH: Частичное обновление данных пользователя.
        """
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'PATCH':
            serializer = UserSerializer(
                request.user, partial=True, data=request.data
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {'message': 'Метод не поддерживается'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


class APISignup(APIView):
    """Создает нового пользователя."""

    permission_classes = (AllowAny,)

    def validate_user_data(self, data):
        """Возвращает валидные данные."""
        serializer = SignUpSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data

    def create_user(self, validated_data):
        """Создает пользователя на основе валидных данных."""
        user, created = CustomUser.objects.get_or_create(**validated_data)
        return user

    def generate_confirmation_code(self, user):
        """Генерирует код подтверждения для пользователя."""
        return default_token_generator.make_token(user)

    def send_confirmation_email(self, email, confirmation_code):
        """Отправляет email с кодом подтверждения на указанный адрес."""
        send_mail(
            subject='Регистрация на сайте YaMDb',
            message=f'Код для подтверждения регистрации: {confirmation_code}',
            from_email=settings.FROM_EMAIL,
            recipient_list=[email],
            fail_silently=True,
        )

    def post(self, request):
        """Обрабатывает POST-запрос для регистрации пользователя."""
        user_data = self.validate_user_data(request.data)
        user = self.create_user(user_data)
        confirmation_code = self.generate_confirmation_code(user)
        self.send_confirmation_email(user.email, confirmation_code)
        return Response(user_data, status=status.HTTP_200_OK)


class APIGetToken(APIView):
    """Работа с JWT токеном."""

    permission_classes = (AllowAny,)

    def validate_request_data(self, request_data):
        """Возвращает вылидные данные из запроса."""
        serializer = GetTokenSerializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data.values()

    def get_user(self, username):
        """Получает пользователя по имени."""
        return get_object_or_404(CustomUser, username=username)

    def check_confirmation_code(self, user, confirmation_code):
        """Проверяет код подтверждения."""
        return default_token_generator.check_token(user, confirmation_code)

    def generate_token(self, user):
        """Генерирует JWT токен для пользователя."""
        return AccessToken.for_user(user)

    def post(self, request):
        """Возвращаем обрабатанный POST-запрос для генерации токена."""
        username, confirmation_code = self.validate_request_data(request.data)
        user = self.get_user(username)
        if not self.check_confirmation_code(user, confirmation_code):
            return Response(
                {'confirmation_code': 'Код подтверждения неверный'},
                status=status.HTTP_400_BAD_REQUEST
            )
        token = self.generate_token(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)
