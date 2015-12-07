from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^gallery/', include('django_flickr_gallery.urls')),
    url(r'^ckeditor/flickr/', include('flickr_ckeditor.urls')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
