from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from reviews.validators import username_validator


ROLES = {
    'user': 'user',
    'admin': 'admin',
    'moderator': 'moderator',
}
USER = ROLES['user']
ADMIN = ROLES['admin']
MODERATOR = ROLES['moderator']


class CustomUser(AbstractUser):
    """Модель переопределенного юзера."""

    roles = [*ROLES.items()]

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
        default=USER,
        max_length=len(max(ROLES.values(), key=len)),
        choices=roles,
    )

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return (f'{self.username} - {self.email} - {self.role}')

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_superuser
