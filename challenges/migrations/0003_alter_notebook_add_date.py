# Generated by Django 4.2.3 on 2024-10-02 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0002_notebook'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notebook',
            name='add_date',
            field=models.DateField(verbose_name='Дата добавления'),
        ),
    ]
