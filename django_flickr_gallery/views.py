# coding: utf-8
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django_flickr_gallery import settings
from django_flickr_gallery.models import FlickrAlbum
from django_flickr_gallery.utils import FlickrPhotoIterator


class FlickrAlbumListView(ListView):
    model = FlickrAlbum
    template_name = settings.LIST_ALBUMS_TEMPLATE
    context_object_name = 'gallery'

    def get_queryset(self):
        queryset = super(FlickrAlbumListView, self).get_queryset()
        return queryset.filter(published=True)


class FlickrAlbumPhotoListView(DetailView):
    model = FlickrAlbum
    template_name = settings.LIST_PHOTOS_TEMPLATE
    context_object_name = 'album'
    context_photos_name = 'photos'
    per_page = settings.PER_PAGE
    per_page_field = settings.PER_PAGE_FIELD

    def get_object(self, queryset=None):
        return get_object_or_404(
            self.model, slug=self.kwargs.get('slug'),
            published=True)

    def get_queryset(self):
        # do a flickr builder and get data
        return FlickrPhotoIterator(
            self.object.flickr_album_id,
            page=self.request.GET.get(self.per_page_field),
            per_page=self.per_page)

    def get_context_data(self, **kwargs):
        context = super(FlickrAlbumPhotoListView, self).get_context_data(**kwargs)
        object_list = self.get_queryset()

        context['object_list'] = object_list
        context[self.context_photos_name] = object_list

        if object_list.has_paginator:
            context[self.context_photos_name] = object_list.paginator.page
            context["paginator"] = object_list.paginator
            context["page"] = object_list.paginator.page

        return context