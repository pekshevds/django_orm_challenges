import json
from datetime import datetime
from typing import Iterable, Any
from django.db import models
from django.db.models import QuerySet
from challenges.utils import obj_to_dict

BRANDS = (
    ("AS", "Asus"),
    ("AP", "Apple"),
    ("HP", "Hewlett-Packard"),
    ("DL", "Dell"),
)

POST_STATUSES = (
    ("NP", "Не опубликован"),
    ("OP", "Опубликован"),
    ("ZB", "Забанен"),
)

POST_CATEGORIES = (
    ("C1", "Категория 1"),
    ("C2", "Категория 2"),
    ("C3", "Категория 3"),
)


class Book(models.Model):
    title = models.CharField(max_length=256)
    author_full_name = models.CharField(max_length=256)
    isbn = models.CharField(max_length=10)

    def __str__(self):
        return self.title


class Notebook(models.Model):
    name = models.CharField(
        max_length=150, unique=True, db_index=True, verbose_name="Наименование"
    )
    brand = models.CharField(
        max_length=2, choices=BRANDS, default="DL", verbose_name="Бренд"
    )
    year_of_release = models.IntegerField(default=2020, verbose_name="Год выпуска")
    ram = models.IntegerField(default=8, verbose_name="Оперативная память (Гб)")
    hdd = models.IntegerField(default=120, verbose_name="Объем жесткого диска (Гб)")
    price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, default=0.0, verbose_name="Цена"
    )
    balance = models.IntegerField(default=0, blank=True, verbose_name="Остаток")
    add_date = models.DateField(verbose_name="Дата добавления")

    def __str__(self) -> str:
        return f"{self.name} {self.brand}/{self.year_of_release}/RAM{self.ram}Gb/HDD{self.hdd}Gb/{self.add_date}"

    @classmethod
    def to_json(cls, data: Iterable | Any) -> str:
        if isinstance(data, QuerySet):
            return json.dumps([obj_to_dict(notebook) for notebook in data], default=str)
        return json.dumps(obj_to_dict(data), default=str)


class Post(models.Model):
    name = models.CharField(max_length=150, verbose_name="Наименование")
    author = models.CharField(max_length=150, verbose_name="Автор")
    status = models.CharField(
        max_length=2, choices=POST_STATUSES, default="NP", verbose_name="Статус"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    published_at = models.DateTimeField(
        verbose_name="Дата публикации", null=True, blank=True
    )
    category = models.CharField(
        max_length=2, choices=POST_CATEGORIES, default="C1", verbose_name="Категория"
    )

    def __str__(self) -> str:
        return f"{self.name} {self.author}/{self.status}/created at {self.created_at}/published at {self.published_at}/{self.category}"

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ) -> Any:
        if self.status == "OP":
            self.published_at = datetime.now()
        return super().save()

    @classmethod
    def to_json(cls, data: Iterable | Any) -> str:
        if isinstance(data, QuerySet):
            return json.dumps([obj_to_dict(post) for post in data], default=str)
        return json.dumps(obj_to_dict(data), default=str)
