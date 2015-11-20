from django.conf.urls import patterns, url

from django_flickr_gallery.views import FlickrAlbumListView
from django_flickr_gallery.views import FlickrAlbumPhotoListView
from django_flickr_gallery.views import CkeditorFlickrView


urlpatterns = patterns('',
    # ckeditor - need be first - don't erase
    url(r'^ckeditor/$', CkeditorFlickrView.as_view(), name='merda-album'),

    url(r'^$', FlickrAlbumListView.as_view(), name='gallery-album'),
    url(r'^(?P<slug>[a-z0-9\-]+)/$', FlickrAlbumPhotoListView.as_view(), name='gallery-photos'),
)
