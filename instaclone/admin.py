from django.contrib import admin
from .models import UserProfile, IGPost, Comment, Like


class UserProfileAdmin(admin.ModelAdmin):
    filter_horizontal = ('followers',)


admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(IGPost)
admin.site.register(Comment)
admin.site.register(Like)
