from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='homepage'),
    path('search/', views.search, name='search'),
    path('posts/new/', views.NewPost, name='new-post'),
    path('<uuid:post_id>/like', views.like, name='like'),
    path('comment/<post_id>/',views.comments, name='comment'),
    path('post/<int:pk>/',views.view_post, name='singlepost'),
]