from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from api_yamdb.consts import LENGTH_150_CHAR, LENGTH_254_CHAR
from reviews.validators import username_validator


class UserRole(models.TextChoices):
    USER = 'user', _('Пользователь')
    ADMIN = 'admin', _('Администратор')
    MODERATOR = 'moderator', _('Модератор')


class User(AbstractUser):
    """Модель переопределенного юзера."""

    username = models.CharField(
        'Юзернейм',
        max_length=LENGTH_150_CHAR,
        unique=True,
        validators=(username_validator,),
    )
    email = models.EmailField(
        'Электронная почта',
        max_length=LENGTH_254_CHAR,
        unique=True,
        help_text=(
            'Укажите уникальный юзернейм. Может содержать до '
            f'{LENGTH_150_CHAR} символов.'
        ),
    )
    bio = models.TextField(
        'О себе',
        blank=True,
    )
    role = models.CharField(
        'Роль',
        max_length=max(len(role) for role in UserRole.values),
        choices=UserRole.choices,
        default=UserRole.USER,
    )

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return f'{self.username} - {self.email} - {self.role}'

    @property
    def is_moderator(self):
        return self.role == UserRole.MODERATOR

    @property
    def is_admin(self):
        return self.role == UserRole.ADMIN or self.is_superuser
