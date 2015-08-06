from django.template.base import Library

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
