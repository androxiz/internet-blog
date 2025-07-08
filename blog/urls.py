from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('article/<int:pk>/', views.article_detail, name='detail'),
    path('article/create/', views.article_create, name='create'),
    path('article/<int:pk>/update/', views.article_update, name='update'),
    path('article/<int:pk>/delete/', views.article_delete, name='delete'),
]
