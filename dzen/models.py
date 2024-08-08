from bleach import clean
from django.core.exceptions import ValidationError
from django.db import models
from bleach.sanitizer import ALLOWED_ATTRIBUTES, ALLOWED_TAGS


# Create your models here.

tags = ALLOWED_TAGS | frozenset(['a', 'code', 'i', 'strong'])
attributes = ALLOWED_ATTRIBUTES.copy()
attributes.update({'a': ['href', 'title']})

class Comment(models.Model):

    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=30)
    email = models.EmailField()
    home_page = models.URLField(null=True, blank=True)
    message = models.TextField()
    main_comment = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='replies',
        on_delete=models.CASCADE
    )

    def clean_message(self):
        clean_message = clean(self.message, tags=tags, attributes=attributes, strip=True)
        if clean_message != self.message:
            raise ValidationError('Сообщение содержит недопустимые HTML-теги или атрибуты!!!!')
        self.message = clean_message

    def save(self, *args, **kwargs):
        self.clean_message()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username}: {self.message[:20]}"