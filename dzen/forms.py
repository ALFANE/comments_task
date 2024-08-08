from captcha.fields import CaptchaField
from django.forms import ModelForm, Textarea, HiddenInput

from dzen.models import Comment


class CommentForm(ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = Comment
        fields = ['username', 'email', 'home_page', 'message', 'captcha', 'main_comment']
        widgets = {
            'message': Textarea(attrs={'rows': 5}),
            'main_comment': HiddenInput(),
        }