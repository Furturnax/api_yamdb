import re

from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.timezone import now
from rest_framework.exceptions import ValidationError

from api_yamdb.consts import (
    CANT_USED_IN_USERNAME,
    SCORE_MAX,
    SCORE_MIN
)


def username_validator(value):
    """Валидатор юзернейна на недопустимые символы и запрещенные слова."""
    if not re.search(r'^[\w.@+-]+\Z', value):
        raise ValidationError(
            (
                'Недопустимые символы в username. '
                'username может содержать только буквы, цифры и '
                'знаки @/./+/-/_.'
            ),
        )
    if value.lower() == CANT_USED_IN_USERNAME:
        raise ValidationError(
            f'Использовать {CANT_USED_IN_USERNAME} как '
            'username запрещено.'
        )


def year_validator(value):
    """Валидатор вводимого года."""
    current_year = now().year
    if value > current_year:
        raise ValidationError('Год не может быть позже текущего года.')


def score_min_validator(value):
    """Валидатор минимальной оценки."""
    return MinValueValidator(
        SCORE_MIN,
        message=f'Нельзя поставить оценку ниже {SCORE_MIN}.',
    )(value)


def score_max_validator(value):
    """Валидатор максимальной оценки."""
    return MaxValueValidator(
        SCORE_MAX,
        message=f'Нельзя поставить оценку выше {SCORE_MAX}.',
    )(value)
