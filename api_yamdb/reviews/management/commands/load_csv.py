import csv

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from django.utils.text import slugify

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User

TABLES = {
    User: 'users.csv',
    Title: 'titles.csv',
    Genre: 'genre.csv',
    Category: 'category.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
    Title.genre.through: 'genre_title.csv',
}


class Command(BaseCommand):
    """
    Пользовательская команда управления Django для загрузки данных
    из CSV-файлов в соответствующие модели.

    Эта команда перебирает словарь моделей и путей к файлам CSV,
    загружая данные из каждого CSV-файла в соответствующую модель Django.

    Использование:
    python manage.py load_csv
    """

    def handle(self, *args, **kwargs):
        """Метод обработки для команды управления."""
        for model, csv_f in TABLES.items():
            csv_path = f'{settings.BASE_DIR}/static/data/{csv_f}'
            self.stdout.write(self.style.SUCCESS(
                f'Загрузка данных для модели {model.__name__} начата'))
            self.load_data(model, csv_path)
            self.stdout.write(self.style.SUCCESS(
                f'Загрузка данных для модели {model.__name__} завершена'))
        self.stdout.write(self.style.SUCCESS('Все данные загружены'))

    def load_data(self, model, csv_path):
        """Загружает данные из CSV-файла в модель Django."""
        with open(csv_path, 'r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            for data in reader:
                self.process_model_data(model, data)
                try:
                    instance = model(**data)
                    instance.save()
                except IntegrityError as e:
                    self.stdout.write(self.style.ERROR(
                        f'Ошибка при сохранении {model.__name__}: {e}'))

    def process_model_data(self, model, data):
        """Обработка данных перед созданием экземпляра модели."""
        if model == Title:
            category, created = Category.objects.get_or_create(
                pk=int(data['category']),
                defaults={'slug': slugify(data['category'])}
            )
            data['category'] = category
        elif model in (Review, Comment):
            self.process_user_data(data)

    def process_user_data(self, data):
        """Обработка данных пользователя."""
        user_id = int(data.get('author', 0))
        user, created = User.objects.get_or_create(pk=user_id)
        if not user_id:
            self.stdout.write(self.style.WARNING(
                'Ключ "author" отсутствует в данных для Review или Comment'))
        data['author'] = user
