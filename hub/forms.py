from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Comment, Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'categories', 'media']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'categories': forms.CheckboxSelectMultiple(),
            'media': forms.ClearableFileInput(attrs={
                'accept': 'image/*,video/*',
                'class': 'comment-media-input'
            }),
        }
        labels = {
            'media': 'Imagem ou vídeo do projeto'
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'media']
        widgets = {
            'text': forms.TextInput(attrs={
                'placeholder': 'Escreva um comentário...',
                'style': 'width: 100%; padding: 0.75rem; background: #f4f4f5; border: none; border-radius: 4px; color: #000;'
            }),
            'media': forms.ClearableFileInput(attrs={
                'accept': 'image/*,video/*',
                'class': 'comment-media-input'
            }),
        }

        labels = {
            'text': 'Legenda',
            'media': 'Foto ou vídeo (opcional)'
        }


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label='E-mail',
        widget=forms.EmailInput(attrs={
            'placeholder': 'voce@empresa.com',
            'autocomplete': 'email'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        labels = {
            'username': 'Nome de usuário',
            'password1': 'Senha',
            'password2': 'Confirme sua senha'
        }
        help_texts = {
            'username': 'Use letras, números e os caracteres @/./+/-/_',
            'password1': 'Mínimo de 8 caracteres, misturando letras e números.',
            'password2': 'Repita a mesma senha para confirmar.'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        field_styles = {
            'username': {'placeholder': 'ex: equipe_streaming'},
            'password1': {'placeholder': 'Crie uma senha segura'},
            'password2': {'placeholder': 'Repita a senha criada'}
        }
        autocomplete_map = {
            'username': 'username',
            'email': 'email',
            'password1': 'new-password',
            'password2': 'new-password'
        }

        for field_name, field in self.fields.items():
            css_classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f"auth-input {css_classes}".strip()
            field.widget.attrs.setdefault('autocomplete', autocomplete_map.get(field_name, field_name))
            if field_name in field_styles:
                for attr, value in field_styles[field_name].items():
                    field.widget.attrs[attr] = value

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
