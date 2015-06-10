from django.conf.urls import patterns, url
from django_flickr_gallery.views import FlickrAlbumListView, FlickrAlbumPhotoListView

urlpatterns = patterns('',
    url(r'^$', FlickrAlbumListView.as_view(), name='gallery-album'),
    url(r'^(?P<slug>[a-z\-]+)/$', FlickrAlbumPhotoListView.as_view(), name='gallery-photos'),
)