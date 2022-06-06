from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Tag, Post, Follow, Stream

# Create your views here.

@login_required
def home(request):
    user = request.user
    # posts = Stream.objects.filter(user=user)
    # group_ids = []
    # for post in posts:
    #     group_ids.append(post.post.id)
    post_items = Post.objects.all()
    post_items.reverse()
    context = {
        'post_items': post_items
    }
    return render(request, 'posts/home.html', context)