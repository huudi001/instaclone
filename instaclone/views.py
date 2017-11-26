import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from . forms import UserCreateForm, PostPictureForm, ProfileEditForm, CommentForm
from . models import UserProfile, IGPost, Comment, Like

@login_required(login_url='/accounts/register')
def index(request):
    if not request.user.is_authenticated():
        redirect('login')


    users_followed = request.user.following.all()
    posts = IGPost.objects.filter(
                user_profile__in=users_followed).order_by('-posted_on')

    return render(request, 'all-upload/index.html')



@login_required
def signup(request):
    form = UserCreateForm()

    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            user = User.objects.get(username=request.POST['username'])
            profile = UserProfile(user=user)
            profile.save()

            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'])
            login(request, new_user)
            return redirect('index')

    return render(request, 'registration/signup.html', {
        'form': form
    })

@login_required
def login_user(request):
    form = AuthenticationForm()

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')

    return render(request, 'registration/login.html', {
        'form': form
    })


def signout(request):
    logout(request)
    return redirect('index')



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


def profile_settings(request, username):
    user = User.objects.get(username=username)
    if request.user != user:
        return redirect('index')

    if request.method == 'POST':
        print(request.POST)
        form = ProfileEditForm(request.POST, instance=user.userprofile, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('profile', kwargs={'username': user.username}))
    else:
        form = ProfileEditForm(instance=user.userprofile)

    context = {
        'user': user,
        'form': form
    }
    return render(request, 'all-uploads/profile_settings.html', context)


def followers(request, username):
    user = User.objects.get(username=username)
    user_profile = UserProfile.objects.get(user=user)
    profiles = user_profile.followers.all()

    context = {
        'header': 'Followers',
        'profiles': profiles,
    }

    return render(request, 'all-upload/follow_list.html', context)


def following(request, username):
    user = User.objects.get(username=username)
    user_profile = UserProfile.objects.get(user=user)
    profiles = user_profile.following.all

    context = {
        'header': 'Following',
        'profiles': profiles
    }
    return render(request, 'all-upload/follow_list.html', context)




def post_picture(request):
    if request.method == 'POST':
        form = PostPictureForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            post = IGPost(user_profile=request.user.userprofile,
                          title=request.POST['title'],
                          image=request.FILES['image'],
                          posted_on=datetime.datetime.now())
            post.save()
            return redirect(reverse('profile', kwargs={'username': request.user.username}))
    else:
        form = PostPictureForm()

    context = {
        'form': form
    }
    return render(request, 'all-upload/post_picture.html', context)


def post(request, pk):
    post = IGPost.objects.get(pk=pk)
    try:
        like = Like.objects.get(post=post, user=request.user)
        liked = 1
    except:
        like = None
        liked = 0

    context = {
        'post': post,
        'liked': liked
    }
    return render(request, 'all-upload/post.html', context)


def likes(request, pk):


    post = IGPost.objects.get(pk=pk)
    profiles = Like.objects.filter(post=post)

    context = {
        'header': 'Likes',
        'profiles': profiles
    }
    return render(request, 'all-upload/follow_list.html', context)



def add_like(request):
    post_pk = request.POST.get('post_pk')
    post = IGPost.objects.get(pk=post_pk)
    try:
        like = Like(post=post, user=request.user)
        like.save()
        result = 1
    except Exception as e:
        like = Like.objects.get(post=post, user=request.user)
        like.delete()
        result = 0

    return {
        'result': result,
        'post_pk': post_pk
    }


def add_comment(request):
    comment_text = request.POST.get('comment_text')
    post_pk = request.POST.get('post_pk')
    post = IGPost.objects.get(pk=post_pk)
    commenter_info = {}

    try:
        comment = Comment(comment=comment_text, user=request.user, post=post)
        comment.save()

        username = request.user.username
        profile_url = reverse('profile', kwargs={'username': request.user})

        commenter_info = {
            'username': username,
            'profile_url': profile_url,
            'comment_text': comment_text
        }


        result = 1
    except Exception as e:
        print(e)
        result = 0

    return {
        'result': result,
        'post_pk': post_pk,
        'commenter_info': commenter_info
    }
