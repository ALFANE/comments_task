from PIL import Image
from bleach import clean
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
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
    attachment = models.FileField(
        upload_to="attachments/",
        null=True,
        blank=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png", "gif", "txt"]
            )
        ],  # Поле для загрузки файла с проверкой допустимых расширений.
    )

    def clean(self):
        super().clean()  # Вызов стандартной валидации.

        if self.attachment:
            if self.attachment.name.endswith(".txt"):
                # Проверка размера текстового файла
                if self.attachment.size > 100 * 1024:  # Ограничение размера файла до 100 КБ
                    raise ValidationError("Текстовый файл не должен превышать 100 КБ.")
            else:
                # Проверка размеров изображения и изменение размера при необходимости
                try:
                    img = Image.open(self.attachment)
                    if img.width > 320 or img.height > 240:
                        output_size = (320, 240)
                        img.thumbnail(output_size)
                        img.save(
                            self.attachment.path
                        )  # Сохранение уменьшенного изображения.
                except Exception as e:
                    raise ValidationError(f"Ошибка обработки изображения: {e}")

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
