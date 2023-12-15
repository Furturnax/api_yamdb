from django.db import models
from users.models import CustomUser

from api_yamdb.consts import (
    LENGTH_50_CHAR,
    LENGTH_256_CHAR,
    MAX_LENGTH
)
from reviews.validators import (
    score_max_validator,
    score_min_validator,
    year_validator
)


class NameSlugModel(models.Model):
    """Модель абстрактного класса NameSlug."""

    name = models.CharField(
        'Название',
        max_length=LENGTH_256_CHAR,
        db_index=True,
    )
    slug = models.SlugField(
        'Slug категории',
        max_length=LENGTH_50_CHAR,
        unique=True,
    )

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return (f'{self.name[:MAX_LENGTH]} - {self.slug}')


class Category(NameSlugModel):
    """Модель класса Категория."""

    class Meta(NameSlugModel.Meta):
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'
        default_related_name = 'categories'


class Genre(NameSlugModel):
    """Модель класса Жанр."""

    class Meta(NameSlugModel.Meta):
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'
        default_related_name = 'genres'


class Title(models.Model):
    """Модель класса Произведение."""

    name = models.CharField(
        'Название',
        max_length=LENGTH_256_CHAR,
    )
    year = models.PositiveSmallIntegerField(
        'Год выпуска',
        validators=[year_validator],
        help_text='Введите год, который не превышает текущий.'
    )
    description = models.TextField(
        'Описание',
        blank=True,
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Slug жанра',
        through='GenreTitle',

    )
    category = models.ForeignKey(
        Category,
        verbose_name='Slug категории',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
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


class GenreTitle(models.Model):
    """Модель промежуточной таблицы GenreTitle."""

    genre = models.ForeignKey(
        Genre,
        verbose_name='Slug жанра',
        on_delete=models.CASCADE,
    )
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return (f'{self.title.name} - {self.genre.name}')


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


class Review(TextAuthorPubdateModel):
    """Модель класса Отзыв."""

    title = models.ForeignKey(
        Title,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
    )
    score = models.PositiveSmallIntegerField(
        'Оценка',
        validators=[score_min_validator, score_max_validator],
        help_text='Введите оценку от 1 до 10.'
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
