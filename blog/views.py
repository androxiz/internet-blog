import os
import openai
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.forms import modelformset_factory
from django.views import View
from django.contrib import messages

from .models import Article, Photo
from .forms import ArticleForm, PhotoForm, RegisterForm
from .utils import generate_text_by_prompt

openai.api_key = os.getenv("OPENAI_API_KEY")


def index(request):
    articles = Article.objects.all().order_by('-created_at')
    return render(request, 'blog/index.html', {'articles': articles})


def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'blog/detail.html', {'article': article})


@login_required
def article_create(request):
    PhotoFormSet = modelformset_factory(Photo, form=PhotoForm, extra=3)

    if request.method == 'POST':
        form = ArticleForm(request.POST)
        formset = PhotoFormSet(request.POST, request.FILES, queryset=Photo.objects.none())

        if form.is_valid() and formset.is_valid():
            article = form.save(commit=False)

            prompt = form.cleaned_data.get('prompt')
            if prompt:
                try:
                    article.content = generate_text_by_prompt(prompt)
                except Exception as e:
                    messages.error(request, f"Помилка генерації тексту через OpenAI: {str(e)}")
                    return render(request, 'blog/article_form.html', {'form': form, 'formset': formset})
            else:
                article.content = form.cleaned_data['content']

            article.author = request.user
            article.save()

            for photo_form in formset:
                if photo_form.cleaned_data:
                    photo = photo_form.save(commit=False)
                    photo.article = article
                    photo.save()

            messages.success(request, "Стаття успішно створена.")
            return redirect('index')
    else:
        form = ArticleForm()
        formset = PhotoFormSet(queryset=Photo.objects.none())

    return render(request, 'blog/article_form.html', {'form': form, 'formset': formset})


@login_required
def article_update(request, pk):
    article = get_object_or_404(Article, pk=pk)

    if request.user != article.author:
        return render(request, '403.html', status=403)

    existing_photos_count = article.photos.count()
    extra_forms = max(3 - existing_photos_count, 0)

    PhotoFormSet = modelformset_factory(Photo, form=PhotoForm, extra=extra_forms, can_delete=True)

    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        formset = PhotoFormSet(request.POST, request.FILES, queryset=article.photos.all())

        if form.is_valid() and formset.is_valid():
            article = form.save(commit=False)

            prompt = form.cleaned_data.get('prompt')
            if prompt:
                try:
                    article.content = generate_text_by_prompt(prompt)
                except Exception as e:
                    messages.error(request, f"Помилка генерації тексту через OpenAI: {str(e)}")
                    return render(request, 'blog/article_form.html', {'form': form, 'formset': formset})
            else:
                article.content = form.cleaned_data['content']

            article.save()

            for photo_form in formset:
                if photo_form.cleaned_data.get('DELETE', False):
                    if photo_form.instance.pk:
                        photo_form.instance.delete()
                else:
                    if photo_form.cleaned_data and photo_form.cleaned_data.get('image'):
                        photo = photo_form.save(commit=False)
                        photo.article = article
                        photo.save()

            messages.success(request, "Стаття оновлена.")
            return redirect('detail', pk=article.pk)
    else:
        form = ArticleForm(instance=article)
        formset = PhotoFormSet(queryset=article.photos.all())

    return render(request, 'blog/article_form.html', {'form': form, 'formset': formset, 'update': True})



@login_required
def article_delete(request, pk):
    article = get_object_or_404(Article, pk=pk)

    if request.user != article.author:
        return render(request, '403.html', status=403)

    if request.method == 'POST':
        article.delete()
        messages.success(request, "Стаття видалена.")
        return redirect('index')

    return render(request, 'blog/article_confirm_delete.html', {'article': article})


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'registration/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Реєстрація успішна.")
            return redirect('index')
        return render(request, 'registration/register.html', {'form': form})


def handler403(request, exception=None):
    return render(request, 'blog/403.html', status=403)


def handler404(request, exception=None):
    return render(request, 'blog/404.html', status=404)


def handler500(request):
    return render(request, 'blog/500.html', status=500)
