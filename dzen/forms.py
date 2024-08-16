from captcha.fields import CaptchaField
from django.forms import ModelForm, Textarea, HiddenInput
from dzen.models import Comment

# Форма для создания и редактирования комментариев, включающая капчу
class CommentForm(ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = Comment
        fields = [
            "username",
            "email",
            "home_page",
            "message",
            "captcha",
            "main_comment",
            "attachment",
        ]
        widgets = {
            "message": Textarea(attrs={"rows": 5}),  # Настройка виджета для поля сообщения
            "main_comment": HiddenInput(),  # Скрытое поле для связи с основным комментарием
        }
