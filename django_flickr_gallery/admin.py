from django.contrib import admin
from django_flickr_gallery.forms import FlickrAlbumForm
from django_flickr_gallery.models import FlickrAlbum


class FlickrAlbumAdmin(admin.ModelAdmin):
    form = FlickrAlbumForm
    list_display = ('title', 'is_published')
    list_filter = ('is_published',)


admin.site.register(FlickrAlbum, FlickrAlbumAdmin)