# coding: utf-8
from django.core.exceptions import ImproperlyConfigured
from django.http.response import JsonResponse
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django_flickr_gallery import settings
from django_flickr_gallery.models import FlickrAlbum
from django_flickr_gallery.utils import FlickrPhotoIterator, FlickrCallException, get_photosets, get_photoset


class CallableQuerysetMixin(object):
    """
    Mixin for handling a callable queryset,
    which will force the update of the queryset.
    Related to issue http://code.djangoproject.com/ticket/8378
    """
    queryset = None

    def get_queryset(self):
        """
        Check that the queryset is defined and call it.
        """
        if self.queryset is None:
            raise ImproperlyConfigured(
                "'%s' must define 'queryset'" % self.__class__.__name__)
        return self.queryset()


class FlickrAlbumListView(CallableQuerysetMixin, ListView):
    model = FlickrAlbum
    template_name = settings.LIST_ALBUMS_TEMPLATE
    context_object_name = 'gallery'
    queryset = FlickrAlbum.published.all

    def get_queryset(self):
        queryset = super(FlickrAlbumListView, self).get_queryset()

        # todo: need to ignore excluded flickr albuns to prevent errors
        exclude_invalids = []
        for album in queryset:
            try:
                album.photoset
            except FlickrCallException:
                exclude_invalids.append(album.id)

        return queryset.exclude(pk__in=exclude_invalids)


class FlickrAlbumPhotoListView(CallableQuerysetMixin, DetailView):
    model = FlickrAlbum
    template_name = settings.LIST_PHOTOS_TEMPLATE
    context_object_name = 'album'
    context_photos_name = 'photos'
    per_page = settings.PER_PAGE
    per_page_field = settings.PER_PAGE_FIELD
    queryset = FlickrAlbum.published.all

    def get_iterator(self):
        # do a flickr builder and get data
        return FlickrPhotoIterator(
            self.object.flickr_album_id,
            page=self.request.GET.get(self.per_page_field),
            per_page=self.per_page)

    def get_context_data(self, **kwargs):
        context = super(FlickrAlbumPhotoListView, self).get_context_data(**kwargs)
        iterator = self.get_iterator()

        context['object_list'] = iterator
        context[self.context_photos_name] = iterator

        if iterator.has_paginator:
            context["photos"] = iterator.paginator.page
            context["paginator"] = iterator.paginator
            context["page"] = iterator.paginator.page

        return context
