from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Recipe


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]

        widgets = {
            'username': forms.TextInput(
                attrs={
                    'placeholder': 'Enter username',
                    'class': 'form-control'
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'placeholder': 'Enter email',
                    'class': 'form-control'
                }
            ),
        }


class RecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        exclude = ['user']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter recipe title'
            }),

            'category': forms.Select(attrs={
                'class': 'form-control'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter recipe description',
                'rows': 4
            }),

            'ingredients': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'List ingredients...',
                'rows': 5
            }),

            'instructions': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter cooking instructions...',
                'rows': 6
            }),

            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].required = False