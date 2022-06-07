from django.shortcuts import get_object_or_404, render, redirect
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
    current_user = request.user
    posts = Post.objects.filter(user=user).all()
    posts.reverse()
    counted = posts.count()
    context = {
        'posts': posts,
        'counted':counted,
        'current_user':current_user
    }
    
    return render(request, 'users/profile.html', context)

@login_required
def profileUsers(request, username):
    user_object = User.objects.get(username=username)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=username).all()
    user_post_length = len(user_posts)
    follower = request.user.username
    user = username

    if FollowersCount.objects.filter(follower=follower, following=user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    user_followers = len(FollowersCount.objects.filter(user=username))
    user_following = len(FollowersCount.objects.filter(follower=username))

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
        'button_text': button_text,
        'user_followers': user_followers,
        'user_following': user_following,
    }
    
    return render(request, 'users/profiler.html', context)



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
    
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']
        
        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/')
        
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/')
    else:
        return redirect('homepage')
        
    

def UserDetail(request, user_id):
    
    user = get_object_or_404(User, id=user_id)
    posts = Post.objects.filter(user=user_id).all()
    counted = posts.count()
    follower = request.user.username
    
    if FollowersCount.objects.filter(follower=follower, user=user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'
        
    followers = FollowersCount.objects.filter(user=user_id).all()
    thefollowers = len(followers)
    following = FollowersCount.objects.filter(follower=user_id).all()
    thefollowing = len(following)
    
    context = {
        'user':user,
        'posts':posts,
        'counted':counted,
        'follower':follower,
        'followers':thefollowers,
        'following':thefollowing,
        
        'button_text':button_text
    }
    return render(request, 'users/user-detail.html', context)