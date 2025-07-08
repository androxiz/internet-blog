from django import forms
from .models import Article, Photo
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ArticleForm(forms.ModelForm):
    prompt = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        help_text="Введіть запит для генерації тексту через ШІ (необов’язково)"
    )

    class Meta:
        model = Article
        fields = ['title', 'content', 'prompt']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'rows': 10, 'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get('content')
        prompt = cleaned_data.get('prompt')

        if not content and not prompt:
            raise forms.ValidationError(
                "Ви повинні або ввести текст статті, або запит для генерації."
            )
        return cleaned_data

class PhotoForm(forms.ModelForm):
    image = forms.ImageField(
        required=False,
        widget=forms.FileInput
    )
    
    class Meta:
        model = Photo
        fields = ['image']
        
        

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ['first_name', 'username', 'password1', 'password2']
