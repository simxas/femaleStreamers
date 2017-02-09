from django.conf.urls import url
from django.contrib import admin

from .views import (
    femalestreamers,
    live_streamers,
    streamers_list,
    streamer_detail,
    stream_detail,
    create_streamer,
)

urlpatterns = [
    url(r'^$', femalestreamers, name='femalestreamers'),
    url(r'^live/$', live_streamers, name='live_list'),
    url(r'^all/$', streamers_list, name='streamers_list'),
    url(r'^create/$', create_streamer, name='create'),
    url(r'^(?P<slug>[\w-]+)/$', streamer_detail, name='detail'),
    url(r'^live/(?P<name>[\w-]+)/$', stream_detail, name='stream_detail'),
    # url(r'^category/(?P<slug>[\w-]+)/$', post_category, name='category'),
    # url(r'^(?P<slug>[\w-]+)/edit/$', post_update, name='update'),
    # url(r'^(?P<slug>[\w-]+)/delete/$', post_delete),
]
