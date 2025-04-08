from django import forms

from webapp.models import Message, Post


class MessageForm(forms.ModelForm):
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
