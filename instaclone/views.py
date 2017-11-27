import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from . models import UserProfile, IGPost, Comment, Like

@login_required(login_url='/accounts/register')
def index(request):
    users_followed = request.user.userprofile.following.all
    posts = IGPost.objects.filter(
                user_profile__in=users_followed).order_by('-posted_on')

    return render(request, 'all-upload/index.html', {
        'posts': posts
    })

@login_required(login_url='/accounts/register')
def profile(request, username):
    user = User.objects.get(username=username)
    if not user:
        return redirect('index')

    profile = UserProfile.objects.get(user=user)
    context = {
        'username': username,
        'user': user,
        'profile': profile
    }
    return render(request, 'all-upload/profile.html', context)
