from django.contrib import admin
from .models import UserProfile, IGPost, Comment, Like


class IGPostAdmin(admin.ModelAdmin):
    filter_horizontal = ('posted_on',)



admin.site.register(IGPost,IGPostAdmin)
admin.site.register(Comment)
admin.site.register(Like)
