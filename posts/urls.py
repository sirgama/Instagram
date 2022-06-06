from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='homepage'),
    path('posts/new/', views.NewPost, name='new-post'),
]