from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^signout/$', views.signout, name='signout'),
    url(r'^profile/(?P<username>[-_\w.]+)/$', views.profile, name='profile'),
    url(r'^profile/(?P<username>[-_\w.]+)/edit/$', views.profile_settings, name='profile_settings'),
    url(r'^profile/(?P<username>[-_\w.]+)/followers/$', views.followers, name='followers'),
    url(r'^profile/(?P<username>[-_\w.]+)/following/$', views.following, name='following'),
    url(r'^post/(?P<pk>\d+)/$', views.post, name='post'),
    url(r'^post/$', views.post_picture, name='post_picture'),
    url(r'^post/(?P<pk>\d+)/likes/$', views.likes, name='likes'),
    url(r'^like/$', views.add_like, name='like'),
    url(r'^comment/$', views.add_comment, name='comment'),
    
]