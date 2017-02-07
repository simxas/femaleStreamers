from django.conf.urls import url
from django.contrib import admin

from .views import (
    live_streamers,
    streamer_detail,
)

urlpatterns = [
    url(r'^$', live_streamers, name='live_list'),
    # url(r'^create/$', post_create, name='create'),
    url(r'^(?P<slug>[\w-]+)/$', streamer_detail, name='detail'),
    # url(r'^category/(?P<slug>[\w-]+)/$', post_category, name='category'),
    # url(r'^(?P<slug>[\w-]+)/edit/$', post_update, name='update'),
    # url(r'^(?P<slug>[\w-]+)/delete/$', post_delete),
]
