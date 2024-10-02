import json
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
