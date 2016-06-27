from django.conf.urls import url

from django_flickr_gallery import settings
from django_flickr_gallery.utils.import_tools import load_view

photoset_list_view = load_view(getattr(settings, 'PHOTOSET_LIST_VIEW'))
photo_list_view = load_view(getattr(settings, 'PHOTO_LIST_VIEW'))


urlpatterns = [
    url(r'^$', photoset_list_view, name='flickr-photoset-list'),
    url(r'^(?P<photoset_id>.+)/$', photo_list_view, name='flickr-photo-list'),
]
