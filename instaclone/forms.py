from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from . models import IGPost, UserProfile, Comment, Like


class UserCreateForm(forms.Form):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class PostPictureForm(forms.Form):
    class Meta:
        model = IGPost
        fields = ['title', 'image']


class ProfileEditForm(forms.Form):
    class Meta:
        model = UserProfile
        fields = ['profile_pic', 'description']


class CommentForm(forms.Form):
    class Meta:
        model = Comment
        fields = ['comment']
