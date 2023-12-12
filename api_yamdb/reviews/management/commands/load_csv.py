import csv

from django.conf import settings
from django.core.management.base import BaseCommand
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import CustomUser

TABLES = {
    CustomUser: 'users.csv',
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
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
        """
        Метод обработки для команды управления.

        Перебирает словарь TABLES, загружает данные из каждого CSV-файла и
        создает экземпляры соответствующей модели Django.
        """
        for model, csv_f in TABLES.items():
            csv_path = f'{settings.BASE_DIR}/static/data/{csv_f}'
            self.load_data(model, csv_path)
        self.stdout.write(self.style.SUCCESS('Все данные успешно загружены'))

    def load_data(self, model, csv_path):
        """Загружает данные из CSV-файла в модель Django."""
        with open(csv_path, 'r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            model.objects.bulk_create(
                model(**data) for data in reader
            )
