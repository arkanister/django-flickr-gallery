"""
Example URLConf for a flickr ckeditor.

Needs set url ``/ckeditor/flickr/`` url to works this app.

    >>> urlpatterns = patterns(''
    >>>     ...
    >>>     url(r'^ckeditor/flickr/', include('flickr_ckeditor.urls')),
    >>>     ...
    >>> )
"""
from django.conf.urls import patterns, url

from flickr_ckeditor.views import CkeditorFlickrView


urlpatterns = patterns('',
    # ckeditor - need be first - don't erase
    url(r'^$', CkeditorFlickrView.as_view(), name='merda-album'),
)