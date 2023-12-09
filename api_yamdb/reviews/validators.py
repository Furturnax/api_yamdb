from django.conf import settings
from rest_framework.exceptions import ValidationError


def username_validator(value):
    """Валидатор юзернейна."""
    if value.lower() == settings.CANT_USED_IN_USERNAME:
        raise ValidationError(
            f'Использовать {settings.CANT_USED_IN_USERNAME} как '
            'username запрещено.'
        )
