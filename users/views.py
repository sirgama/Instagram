from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from posts.models import Post
from django.contrib.auth.models import User
from .models import Profile
from posts.models import FollowersCount

# Create your views here.

def register(request):
    
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            return redirect('edit-account')
        
    else:
        form = UserRegisterForm()
            
    return render(request, 'users/register.html', {"form":form})

@login_required
def profile(request):
    user = request.user
    posts = Post.objects.filter(user=user).all()
    posts.reverse()
    counted = posts.count()
    context = {
        'posts': posts,
        'counted':counted
    }
    
    return render(request, 'users/profile.html', context)

# def profileUsers(request, pk):
#     user_object = User.objects.get(username=pk)
#     user_profile = Profile.objects.get(user=user_object)
#     user_posts = Post.objects.filter(user=pk).all()
#     user_post_length = len(user_posts)
#     follower = request.user.username
#     user = pk

#     if Follow.objects.filter(follower=follower, following=user).first():
#         button_text = 'Unfollow'
#     else:
#         button_text = 'Follow'

#     user_followers = len(Follow.objects.filter(user=pk))
#     user_following = len(Follow.objects.filter(follower=pk))

#     context = {
#         'user_object': user_object,
#         'user_profile': user_profile,
#         'user_posts': user_posts,
#         'user_post_length': user_post_length,
#         'button_text': button_text,
#         'user_followers': user_followers,
#         'user_following': user_following,
#     }
    
#     return render(request, 'users/profile.html', context)

@login_required
def edit_account(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if u_form.is_valid and p_form.is_valid:
            u_form.save()
            p_form.save()
            messages.success(request, f'Account updated')
            return redirect('profile')
        
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'u_form' : u_form,
        'p_form' : p_form
    }
    
    return render(request, 'users/edit_account.html', context)

def follow(request):
    
    pass