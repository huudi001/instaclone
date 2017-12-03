from django.shortcuts import render,redirect
from django.http import Http404
from django.contrib.auth.decorators import login_required
from .models import Profile, Tag, Post, Follow, Comment, Like
from django.core.exceptions import ObjectDoesNotExist
from .forms import NewPostForm, NewCommentForm

@login_required(login_url='/accounts/register')
def timeline(request):

    current_user = request.user

    title = 'Home'

    following = Follow.get_following(current_user.id)

    posts = Post.get_posts()

    following_posts = []

    for follow in following:

        for post in posts:

            if follow.profile == post.profile:

                following_posts.append(post)

    return render(request, 'all-uploads/timeline.html', {"title": title, "following": following, "user":current_user, "following_posts":following_posts})
@login_required(login_url='/accounts/register')
def profile(request,id):

    current_user = request.user

    try:

        single_profile = Profile.objects.get(user=current_user.id)

        title = f'{current_user.username}'

        posts = Post.objects.filter(user=current_user.id)

        return render(request, 'all-uploads/profile.html', {"title":title,"current_user":current_user,"posts":posts})

    except ObjectDoesNotExist:
        raise Http404()


@login_required(login_url='/accounts/register')
def new_post(request):
    current_user = request.user
    current_profile = current_user.profile
    if request.method == 'POST':
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid:
            post = form.save(commit=False)
            post.user = current_user
            post.profile = current_profile
            post.save()
            return redirect(profile, current_user.id)
    else:
        form = NewPostForm()

    title = 'Create Post'

    return render(request,'all-uploads/new-post.html', {"form":form})

@login_required(login_url='/accounts/register')
def explore(request,id):

    current_user = request.user

    current_user_profile = current_user.profile

    profiles = Profile.get_all_other_profiles(current_user.id)

    title = f'{current_user.username} explore'

    return render(request,'all-uploads/explore.html',{"title":title,"profiles":profiles})

@login_required(login_url='/accounts/register')
def follow(request,id):

    current_user = request.user

    follow_profile = Profile.objects.get(id=id)

    following = Follow(user=current_user, profile=follow_profile)

    following.save()

    return redirect(timeline)

@login_required(login_url='/accounts/register')
def new_comment(request,id):

    current_user = request.user

    current_post = Post.objects.get(id=id)

    if request.method == 'POST':

        form = NewCommentForm(request.POST)

        if form.is_valid:

            comment = form.save(commit=False)

            comment.user = current_user

            comment.post = current_post

            comment.save()

            return redirect(post,current_post.id)

    else:

        form = NewCommentForm()

    title = f'Comment {current_post.user.username}\'s Post'

    return render(request,'all-uploads/new-comment.html', {"title":title,"form":form,"current_post":current_post})

@login_required(login_url='/accounts/register')
def like(request,id):

    current_user = request.user

    current_post = Post.objects.get(id=id)

    like = Like(user=current_user,post=current_post,likes_number=1)

    like.save()

    return redirect(post,current_post.id)

@login_required(login_url='/accounts/register')
def post(request,id):

    current_user = request.user
    try:
        current_post = Post.objects.get(id=id)

        title = f'{current_post.user.username}\'s post'

        comments = Comment.get_post_comments(id)

        likes = Like.num_likes(id)

        like = Like.objects.filter(post=id).filter(user=current_user)

    except DoesNotExist:
        raise Http404()

    return render(request, 'all-uploads/post.html', {"title":title, "post":current_post,"comments":comments,"likes":likes,"like":like })
