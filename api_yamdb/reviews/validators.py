import re

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.timezone import now
from rest_framework.exceptions import ValidationError


def username_validator(value):
    """Валидатор юзернейна."""
    regex = r"^[\w.@+-]+\Z"
    if re.search(regex, value) is None:
        invalid_characters = set(re.findall(r"[^\w.@+-]", value))
        raise ValidationError(
            (
                f"Не допустимые символы {invalid_characters} в username. "
                f"username может содержать только буквы, цифры и "
                f"знаки @/./+/-/_."
            ),
        )
    if value.lower() == settings.CANT_USED_IN_USERNAME:
        raise ValidationError(
            f'Использовать {settings.CANT_USED_IN_USERNAME} как '
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
        settings.SCORE_MIN,
        message=f'Нельзя поставить оценку ниже {settings.SCORE_MIN}.',
    )(value)


def score_max_validator(value):
    """Валидатор максимальной оценки."""
    return MaxValueValidator(
        settings.SCORE_MAX,
        message=f'Нельзя поставить оценку выше {settings.SCORE_MAX}.',
    )(value)
