from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from reviews.validators import username_validator
from users.enums import Roles


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
        max_length=settings.LENGTH_254_CHAR,
        unique=True,
        help_text=(
            'Укажите уникальный юзернейм. Может содержать до '
            f'{settings.LENGTH_150_CHAR} символов.')
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

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return (f'{self.username} - {self.email} - {self.role}')

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
