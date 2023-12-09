from enum import Enum

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from reviews.validators import username_validator


class Roles(Enum):
    """Перечисление ролей пользователя."""

    USER = "user"
    ADMIN = "admin"
    MODERATOR = "moderator"

    def __str__(self):
        return self.value

    @classmethod
    def choices(cls):
        """Получить список выборов для поля модели."""
        return [(role.value, role.name) for role in cls]

    @classmethod
    def max_length(cls):
        """Максимальная длина для поля модели."""
        return max(len(role.value) for role in cls)


class CustomUser(AbstractUser):
    """Модель переопределенного юзера."""

    username = models.CharField(
        'Юзернейм',
        max_length=settings.LENGTH_150_CHAR,
        unique=True,
        validators=[username_validator],
    )
    email = models.EmailField(
        'Электронная почта',
        max_length=settings.LENGTH_256_CHAR,
        unique=True,
    )
    bio = models.TextField(
        'О себе',
        blank=True,
    )
    role = models.CharField(
        'Роль',
        default=Roles.USER.value,
        max_length=Roles.max_length(),
        choices=Roles.choices(),
    )

    @property
    def is_user(self):
        """Проверяет, имеет ли пользователь роль USER."""
        return self.role == Roles.USER.value

    @property
    def is_moderator(self):
        """Проверяет, имеет ли пользователь роль MODERATOR."""
        return self.role == Roles.MODERATOR.value

    @property
    def is_admin(self):
        """Проверяет, имеет ли пользователь роль ADMIN."""
        return self.role == Roles.ADMIN.value or self.is_superuser

    def __str__(self):
        return (f'{self.username} - {self.email} - {self.role}')

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)
