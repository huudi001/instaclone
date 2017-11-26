from datetime import datetime
from django.db import models
from django.contrib.auth.models import User, BaseUserManager, AbstractBaseUser, PermissionsMixin
from datetime import datetime

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    followers = models.ManyToManyField('UserProfile',related_name="followers_profile",blank=True)
    following = models.ManyToManyField('UserProfile',related_name="following_profile", blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics',null=True,blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)

    def get_number_of_followers(self):
        print(self.followers.count())
        if self.followers.count():
            return self.followers.count()
        else:  
            return 0

    def get_number_of_following(self):
        print(self.following.count())
        if self.following.count():
            return self.following.count()
        else:
            return 0

    def __str__(self):
        return self.user.username

class IGPost(models.Model):
    user_profile = models.ForeignKey(UserProfile, null=True, blank=True)
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='posts')
    posted_on = models.DateTimeField(default=datetime.now)

    def get_number_of_likes(self):
        return self.like_set.count()

    def get_number_of_comments(self):
        return self.comment_set.count()

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('IGPost')
    user = models.ForeignKey(User)
    comment = models.CharField(max_length=100)
    posted_on = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.comment


class Like(models.Model):
    post = models.ForeignKey('IGPost')
    user = models.ForeignKey(User)

    class Meta:
        unique_together = ("post", "user")

    def __str__(self):
        return 'Like: ' + self.user.username + ' ' + self.post.title
