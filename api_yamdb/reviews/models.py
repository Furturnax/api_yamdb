from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from api_yamdb.consts import (
    LENGTH_50_CHAR,
    LENGTH_256_CHAR,
    MAX_LENGTH,
    SCORE_MAX,
    SCORE_MIN
)
from reviews.validators import year_validator
from users.models import User


class NameSlugModel(models.Model):
    """Модель абстрактного класса NameSlug."""

    name = models.CharField(
        'Название',
        max_length=LENGTH_256_CHAR,
        db_index=True,
    )
    slug = models.SlugField(
        'Слаг названия',
        max_length=LENGTH_50_CHAR,
        unique=True,
    )

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return f'{self.name[:MAX_LENGTH]} - {self.slug}'


class Category(NameSlugModel):
    """Модель класса Категория."""

    class Meta(NameSlugModel.Meta):
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Genre(NameSlugModel):
    """Модель класса Жанр."""

    class Meta(NameSlugModel.Meta):
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Модель класса Произведение."""

    name = models.CharField(
        'Название',
        max_length=LENGTH_256_CHAR,
    )
    year = models.SmallIntegerField(
        'Год выпуска',
        validators=(year_validator,),
        help_text='Введите год, который не превышает текущий.',
        db_index=True
    )
    description = models.TextField(
        'Описание',
        blank=True,
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Слаг жанра',

    )
    category = models.ForeignKey(
        Category,
        verbose_name='Слаг категории',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'
        default_related_name = 'titles'
        ordering = ('name',)

    def __str__(self):
        return (
            f'{self.name[:MAX_LENGTH]} - '
            f'{self.description[:MAX_LENGTH]} - '
            f'{self.year} - '
            f'{self.genre.name} - '
            f'{self.category.name}'
        )


class TextAuthorPubdateModel(models.Model):
    """Модель абстрактного класса TextAuthorPubdateModel."""

    text = models.TextField(
        'Текст',
    )
    author = models.ForeignKey(
        User,
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


class Review(TextAuthorPubdateModel):
    """Модель класса Отзыв."""

    title = models.ForeignKey(
        Title,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
    )
    score = models.PositiveSmallIntegerField(
        'Оценка',
        validators=(
            MinValueValidator(
                SCORE_MIN,
                message=f"Нельзя поставить оценку ниже {SCORE_MIN}.",
            ),
            MaxValueValidator(
                SCORE_MAX,
                message=f"Нельзя поставить оценку выше {SCORE_MAX}.",
            ),
        ),
        help_text=f'Введите оценку от {SCORE_MIN} до {SCORE_MAX}.'
    )

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'
        default_related_name = 'reviews'
        constraints = [
            models.UniqueConstraint(
                name='%(app_label)s_%(class)s_unique_review',
                fields=['author', 'title'],
            ),
        ]

    def __str__(self):
        return (
            f'{self.title[:MAX_LENGTH]} - '
            f'{self.text[:MAX_LENGTH]} - '
            f'{self.author.username} - '
            f'{self.score} - '
            f'{self.pub_date}'
        )


class Comment(TextAuthorPubdateModel):
    """Модель класса Комментарий."""

    review = models.ForeignKey(
        Review,
        verbose_name='Оценка',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'

    def __str__(self):
        return (
            f'{self.review.title[:MAX_LENGTH]} - '
            f'{self.text[:MAX_LENGTH]} - '
            f'{self.author.username} - '
            f'{self.pub_date}'
        )
