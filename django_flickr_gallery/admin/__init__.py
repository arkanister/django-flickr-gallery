from django.contrib import admin
from django_flickr_gallery.admin.album import FlickrAlbumAdmin
from django_flickr_gallery.admin.category import CategoryAdmin
from django_flickr_gallery.models import FlickrAlbum
from django_flickr_gallery.models import Category

admin.site.register(FlickrAlbum, FlickrAlbumAdmin)
admin.site.register(Category, CategoryAdmin)
