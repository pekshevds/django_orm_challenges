"""
В этом задании вам предстоит работать с моделью поста в блоге. У него есть название, текст, имя автора, статус
(опубликован/не опубликован/забанен), дата создания, дата публикации, категория (одна из нескольких вариантов).

Ваша задача:
- создать соответствующую модель (в models.py)
- создать и применить миграцию по созданию модели (миграцию нужно добавить в пул-реквест)
- заполнить вашу локальную базу несколькими ноутбуками для облегчения тестирования
- реализовать у модели метод to_json, который будет преобразовывать объект книги в json-сериализуемый словарь
- по очереди реализовать каждую из вьюх в этом файле, проверяя правильность их работу в браузере
"""

from datetime import datetime, timedelta
from django.http import HttpRequest, HttpResponse
from challenges.models import Post


def last_posts_list_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть 3 последних опубликованных поста.
    """
    return HttpResponse(
        Post.to_json(Post.objects.filter(status="OP").order_by("-created_at")[:3])
    )


def posts_search_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть все посты, которые подходят под поисковый запрос.
    Сам запрос возьмите из get-параметра query.
    Подходящесть поста можете определять по вхождению запроса в название или текст поста, например.
    """
    query = request.GET.get("q")
    return HttpResponse(Post.to_json(Post.objects.filter(post__icontains=query)))


def untagged_posts_list_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть все посты без категории, отсортируйте их по автору и дате создания.
    """
    return HttpResponse(
        Post.to_json(
            Post.objects.filter(category="").order_by("author").order_by("created_at")
        )
    )


def categories_posts_list_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть все посты все посты, категория которых принадлежит одной из указанных.
    Возьмите get-параметр categories, в нём разделённый запятой список выбранных категорий.
    """
    categories = request.GET.get("categories").split(",")
    return HttpResponse(Post.to_json(Post.objects.filter(category__in=categories)))


def last_days_posts_list_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть посты, опубликованные за последние last_days дней.
    Значение last_days возьмите из соответствующего get-параметра.
    """

    last_days = int(request.GET.get("last_days"))
    if last_days == 0:
        date = datetime.now()
    else:
        delta = datetime.now().date() - timedelta(days=last_days)
        date = datetime(year=delta.year, month=delta.month, day=delta.day)
    return HttpResponse(
        Post.to_json(Post.objects.filter(status="OP").filter(created_at__lt=date))
    )
