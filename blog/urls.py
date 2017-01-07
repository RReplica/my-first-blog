from django.conf.urls import url
from django.contrib import admin
from posts import views as posts_views

urlpatterns = [
    url(r'^$', posts_views.post_list, name="list"),
    url(r'^create/$', posts_views.post_create),
    url(r'^(?P<id>\d+)/$', posts_views.post_detail, name="detail"),
    url(r'^(?P<id>\d+)/edit/$', posts_views.post_update, name="update"),
    url(r'^(?P<id>\d+)/delete$', posts_views.post_delete),
]
