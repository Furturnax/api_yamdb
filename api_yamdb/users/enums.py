from enum import Enum


class Roles(Enum):
    """Перечисление ролей пользователя."""

    USER = 'User'
    ADMIN = 'Admin'
    MODERATOR = 'Moderator'

    def __str__(self):
        return self.value

    @classmethod
    def choices(cls):
        """Получить список выборов для поля модели."""
        return [(role.value, role.name) for role in cls]

    @classmethod
    def max_length(cls):
        """Максимальная длина для поля модели."""
        return max(len(role.value) for role in cls)
