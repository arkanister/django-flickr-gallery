from django.conf.urls import patterns, url
from django_flickr_gallery.views import FlickrAlbumListView, FlickrAlbumPhotoListView

urlpatterns = patterns('',
    url(r'^$', FlickrAlbumListView.as_view(), name='flickr-album-list'),
    url(r'^photos/(?P<pk>\d+)/$', FlickrAlbumPhotoListView.as_view(), name='flickr-album-photo-list'),
)