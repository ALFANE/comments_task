from bleach import clean
from django.core.exceptions import ValidationError
from django.db import models
from bleach.sanitizer import ALLOWED_ATTRIBUTES, ALLOWED_TAGS


# Определение наборов допустимых HTML-тегов и атрибутов для очистки пользовательского ввода.
tags = ALLOWED_TAGS | frozenset(["a", "code", "i", "strong"])
attributes = ALLOWED_ATTRIBUTES.copy()
attributes.update({"a": ["href", "title"]})


# Модель Comment представляет структуру данных для хранения комментариев.
class Comment(models.Model):
    # Определение полей модели.
    id = models.AutoField(
        primary_key=True
    )  # Уникальный идентификатор для каждого комментария.
    username = models.CharField(
        max_length=30
    )  # Имя пользователя, оставившего комментарий.
    email = models.EmailField()  # Email-адрес пользователя.
    home_page = models.URLField(
        null=True, blank=True
    )  # Опциональное поле для домашней страницы пользователя.
    message = models.TextField()  # Содержимое комментария.
    main_comment = models.ForeignKey(
        "self", null=True, blank=True, related_name="replies", on_delete=models.CASCADE
    )  # Ссылка на основной комментарий, если это ответ на другой комментарий.
    created_at = models.DateTimeField(
        auto_now_add=True, null=True
    )  # Время создания комментария.
    updated_at = models.DateTimeField(
        auto_now=True, null=True
    )  # Время последнего обновления комментария.

    # Метод для очистки текста комментария от недопустимых HTML-тегов и атрибутов.
    def clean_message(self):
        clean_message = clean(
            self.message, tags=tags, attributes=attributes, strip=True
        )
        if clean_message != self.message:
            raise ValidationError(
                "Сообщение содержит недопустимые HTML-теги или атрибуты."
            )
        self.message = clean_message

    # Переопределение метода сохранения модели для автоматической очистки текста перед сохранением.
    def save(self, *args, **kwargs):
        self.clean_message()
        super().save(*args, **kwargs)

    # Представление объекта в виде строки, используемое, например, в админке Django.
    def __str__(self):
        return f"{self.username}: {self.message[:20]}"
