import re

from django.utils.timezone import now
from rest_framework.exceptions import ValidationError

from api_yamdb.consts import CANT_USED_IN_USERNAME


def username_validator(value):
    """Валидатор юзернейна на недопустимые символы и запрещенные слова."""
    cleaned_value = re.sub(r'[^\w.@+-]', '', value)
    if set(value) - set(cleaned_value):
        invalid_characters = set(value) - set(cleaned_value)
        raise ValidationError(
            f'Недопустимые символы {"".join(invalid_characters)}в username. '
            'username может содержать только буквы, цифры и '
            'знаки @/./+/-/_.'
        )
    if value.lower() == CANT_USED_IN_USERNAME:
        raise ValidationError(
            f'Использовать {CANT_USED_IN_USERNAME} как '
            'username запрещено.'
        )
    return value


def year_validator(value):
    """Валидатор вводимого года."""
    current_year = now().year
    if value > current_year:
        raise ValidationError('Год не может быть позже текущего года.')
    return value
