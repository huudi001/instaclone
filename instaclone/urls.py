from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^post/$', views.post_picture, name='post_picture'),
    url(r'^post/(?P<pk>\d+)/likes/$', views.likes, name='likes'),
    url(r'^like/$', views.add_like, name='like'),
    url(r'^comment/$', views.add_comment, name='comment'),

]
