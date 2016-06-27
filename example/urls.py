from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^', include('example.website.urls')),
    url(r'^gallery/', include('django_flickr_gallery.urls')),
    url(r'^ckeditor/flickr/', include('flickr_ckeditor.urls')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),

    url(r'^admin/', include(admin.site.urls)),
]
