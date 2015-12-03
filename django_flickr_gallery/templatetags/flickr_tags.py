from django.template import Library
from django_flickr_gallery.models.album import FlickrAlbum

from django_flickr_gallery.utils import FlickrPhotoIterator
from django_flickr_gallery.settings import PER_PAGE_FIELD

register = Library()


@register.inclusion_tag("gallery/flickr/tags/dummy.html", takes_context=True)
def show_flickr_photoset(context, photoset_id, page=None, per_page=None, template="gallery/flickr/photoset.html"):
    request = context['request']

    # get page number
    if per_page is not None:
        page = page or request.GET.get(PER_PAGE_FIELD, None)

    object_list = FlickrPhotoIterator(photoset_id, page=page, per_page=per_page)

    context.update({
        'photos': object_list,
        'object_list': object_list,
        'template': template
    })

    if object_list.has_paginator:
        context.update({
            "paginator": object_list.paginator,
            "page": object_list.paginator.page,
            "photos": object_list.paginator.page
        })

    return context


@register.inclusion_tag("gallery/flickr/tags/dummy.html", takes_context=True)
def show_flickr_photoset_featured(context, count=3, count_photos=10, template="gallery/flickr/tags/featured.html"):
    object_list = []

    for album in FlickrAlbum.featured.all()[:count]:
        photos = FlickrPhotoIterator(album.flickr_album_id).photos[:count_photos]
        object_list.append((album, photos))

    context.update({
        'featured': object_list,
        'template': template
    })

    return context


@register.inclusion_tag('gallery/flickr/tags/dummy.html', takes_context=True)
def paginator(context, page, template='gallery/flickr/tags/pagination.html', adjacent_pages=2):
    """
    To be used in conjunction with the object_list generic view.

    Adds pagination context variables for use in displaying first, adjacent and
    last page links in addition to those created by the object_list generic
    view.
    """
    page_range = [n for n in range(
        page.number - adjacent_pages,
        page.number + adjacent_pages + 1) if 0 < n <= page.paginator.num_pages]

    return {
        'page': page,
        'page_range': page_range,
        'request': context['request'],
        'template': template}