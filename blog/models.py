from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Photo(models.Model):
    image = models.ImageField(upload_to='article_photos/', blank=True, null=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='photos')
