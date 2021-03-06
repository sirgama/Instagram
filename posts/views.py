from multiprocessing import context
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import Tag, Post, FollowersCount,  Likes, Comments
from django.contrib.auth.models import User
from .forms import NewPostForm
from django.urls import reverse
from users.models import Profile

# Create your views here.

@login_required
def home(request):
    user = request.user
    post_items = Post.objects.all()
    all_users = User.objects.all()
    
    comments = Comments.objects.all()
    context = {
        'post_items': post_items[::-1],
        'all_users':all_users[::-1],
        'user':user,
        'comments':comments
       
    }
    return render(request, 'posts/home.html', context)

@login_required
def NewPost(request):
    user = request.user.id
    tags_objs = []
    
    if request.method == 'POST':
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            picture = form.cleaned_data.get('picture')
            caption = form.cleaned_data.get('caption')
            tag_form = form.cleaned_data.get('tag')
            tags_list = list(tag_form.split(','))
            
            for tag in tags_list:
                t, created = Tag.objects.get_or_create(title=tag)
                tags_objs.append(t)
            p, created = Post.objects.get_or_create(picture=picture, caption=caption, user_id=user)
            p.tags.set(tags_objs)
            p.save()
            return redirect('homepage')
    else:
        form = NewPostForm()
    context = {
        'form': form
    }
    return render(request, 'posts/new_post.html', context)
            
def like(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    current_likes = post.likes
    liked = Likes.objects.filter(user=user, post=post).count()
    if not liked:
        liked = Likes.objects.create(user=user, post=post)
        current_likes = current_likes + 1
    else:
        liked = Likes.objects.filter(user=user, post=post).delete()
        current_likes = current_likes - 1
    
    post.likes = current_likes
    post.save()
    
    return HttpResponseRedirect(reverse('homepage'))
        
def comments(request, post_id):
    user = request.user
    if request.method == 'POST':
        comment = request.POST.get('comment')
        post = Post.objects.get(id=post_id)
        user_profile = User.objects.get(username=user.username)
        Comments.objects.create(comment = comment, post=post, user=user_profile)
    return HttpResponseRedirect(reverse('homepage'))
        

@login_required
def view_post(request,pk):
    post = Post.objects.get(id=pk)
    try:
        comments = Comments.filter_comments_by_post_id(pk)
                
    except:  
        comments = None
    
    context = {
        'post':post,
        "comments":comments
        }   
    return render(request,'posts/singlepost.html',context)
        
def search(request):
    if 'post' in request.GET and request.GET["post"]:
        search_term = request.GET.get("post")
        searched_posts = Post.search_by_caption(search_term)
        message = f"{search_term}"

        return render(request, 'posts/search.html',{"message":message,"captions": searched_posts})

    else:
        message = "You haven't searched for any term"
        return render(request, 'posts/search.html',{"message":message})
    

def PostDetail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    context = {
        'post':post
    }
    return render(request, 'posts/post-detail.html', context)
    