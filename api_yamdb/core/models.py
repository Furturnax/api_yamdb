from django.conf import settings
from django.db import models

from users.models import CustomUser


class NameSlugModel(models.Model):
    """Модель абстрактного класса NameSlug."""

    name = models.CharField(
        'Название',
        max_length=settings.LENGTH_256_CHAR,
    )
    slug = models.SlugField(
        'Slug категории',
        max_length=settings.LENGTH_50_CHAR,
        unique=True,
    )

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return (f'{self.name[:settings.MAX_LENGTH]} - {self.slug}')


class TextAuthorPubdateModel(models.Model):
    """Модель абстрактного класса TextAuthorPubdateModel."""

    text = models.TextField(
        'Текст',
    )
    author = models.ForeignKey(
        CustomUser,
        verbose_name='Автор',
        on_delete=models.CASCADE,
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        abstract = True
        ordering = ('pub_date',)
