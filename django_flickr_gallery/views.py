# coding: utf-8
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django_flickr_gallery import settings
from django_flickr_gallery.models import FlickrAlbum
from django_flickr_gallery.utils import FlickrPhotoPaginator


class FlickrAlbumListView(ListView):
    model = FlickrAlbum
    template_name = settings.LIST_ALBUMS_TEMPLATE
    context_object_name = 'flickr_albums'

    def get_queryset(self):
        queryset = super(FlickrAlbumListView, self).get_queryset()
        return queryset.filter(is_published=True)


class FlickrAlbumPhotoListView(DetailView):
    model = FlickrAlbum
    template_name = settings.LIST_PHOTOS_TEMPLATE
    context_object_name = 'flickr_album'
    per_page = settings.PER_PAGE
    per_page_field = settings.PER_PAGE_FIELD

    def get_object(self, queryset=None):
        return self.model.objects.get(pk=self.kwargs.get('pk'), is_published=True)

    def get_paginator(self):
        return FlickrPhotoPaginator(self.object,
             page=self.request.GET.get(self.per_page_field),
             per_page=self.per_page)

    def get_context_data(self, **kwargs):
        context = super(FlickrAlbumPhotoListView, self).get_context_data(**kwargs)
        paginator = self.get_paginator()
        context["photos"] = paginator.page
        context["paginator"] = paginator
        return context