from django import forms
from .models import *


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text']

class RegistrationUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'nickname', 'description', 'link_fb',
            'whatsapp', 'telegram', 'photo'
        ]

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'name',
            'photo',
        ]




