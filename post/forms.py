from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from multiupload.fields import MultiMediaField
import re
from .models import *


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']


class PostForm(forms.ModelForm):
    tag_names = forms.CharField(required=False)
    images = MultiMediaField(min_num=1, max_num=5)

    class Meta:
        model = Post
        fields = ['author', 'images', 'caption', 'is_published', 'tag_names']
        widgets = {
            'caption': forms.Textarea(attrs={'cols': 60, 'rows': 10})
        }

    def save(self, commit=True, author=None, *args, **kwargs):
        post = super().save(commit=False)
        post.author = author
        post.save()

        for image in self.cleaned_data['images']:
            Image.objects.create(post=post, image=image)

        tag_names = self.cleaned_data.get('tag_names')
        if tag_names:
            tag_names = re.split(', #', tag_names)
            for name in tag_names:
                name = name.strip()
                tag, _ = Tag.objects.get_or_create(name=name)
                post.tags.add(tag)

        return post


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'form-input'}))
    avatar = forms.ImageField(label='Avatar', widget=forms.ClearableFileInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    full_name = forms.CharField(label='Full Name', widget=forms.TextInput(attrs={'class': 'form-input'}),  required=False)
    bio = forms.CharField(label='Bio', widget=forms.Textarea(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'avatar', 'email', 'password1', 'password2', 'full_name', 'bio',)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")

        return password2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].validators = []



class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


