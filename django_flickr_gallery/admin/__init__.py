from django.contrib import admin
from django_flickr_gallery.admin.photoset import PhotosetAdmin
from django_flickr_gallery.models import Photoset


admin.site.register(Photoset, PhotosetAdmin)
