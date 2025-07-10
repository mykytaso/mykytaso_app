from django import forms
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox

from webapp.models import Message, Post


class MessageForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

    class Meta:
        model = Message
        fields = ["email", "content"]
        labels = {
            "email": "Your Email Address",
            "content": "Your Message",
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["cover_image", "cover_title", "cover_description"]
