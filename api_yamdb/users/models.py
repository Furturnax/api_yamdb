from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from api_yamdb.consts import LENGTH_EMAIL, LENGTH_USERNAME
from reviews.validators import username_validator


class User(AbstractUser):
    """Модель переопределенного юзера."""

    class Role(models.TextChoices):
        """Класс определенных ролей."""

        USER = 'user', _('Пользователь')
        ADMIN = 'admin', _('Администратор')
        MODERATOR = 'moderator', _('Модератор')

    username = models.CharField(
        'Юзернейм',
        max_length=LENGTH_USERNAME,
        unique=True,
        validators=(username_validator,),
    )
    email = models.EmailField(
        'Электронная почта',
        max_length=LENGTH_EMAIL,
        unique=True,
        help_text=(
            'Укажите уникальный юзернейм. Может содержать до '
            f'{LENGTH_USERNAME} символов.'
        ),
    )
    bio = models.TextField(
        'О себе',
        blank=True,
    )
    role = models.CharField(
        'Роль',
        max_length=max(len(role) for role in Role.values),
        choices=Role.choices,
        default=Role.USER,
    )

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return f'{self.username} - {self.email} - {self.role}'

    @property
    def is_moderator(self):
        return self.role == self.Role.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN or self.is_superuser
