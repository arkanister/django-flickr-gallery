# -*- coding: utf-8 -*-
from __future__ import with_statement
from django.template.base import (Node, Library, TemplateSyntaxError)
from django.template.loader import get_template
from django_flickr_gallery.utils import FlickrPhotoPaginator
from django_flickr_gallery import settings

import re

register = Library()


kwarg_re = re.compile(r"(?:(\w+)=)?(.+)")


class ShowFlickrPhotosetNode(Node):
    per_page = settings.PER_PAGE
    per_page_field = settings.PER_PAGE_FIELD

    def __init__(self, photoset_id, template):
        self.template = template or "gallery/flickr/photoset.html"
        self.photoset_id = photoset_id

    def render(self, context):
        photoset_id = self.photoset_id.resolve(context)

        try:
            template = self.template.resolve(context)
        except AttributeError:
            template = self.template

        t = get_template(self.template)
        return t.render(self.get_context(context, photoset_id))

    def get_paginator(self, photoset_id, request=None):
        if request is None:
            return FlickrPhotoPaginator(photoset_id)

        return FlickrPhotoPaginator(
            photoset_id,
            page=request.GET.get(self.per_page_field),
            per_page=self.per_page)

    def get_context(self, context, photoset_id):
        try:
            # If there's an exception (500), default context_processors may not be called.
            request = context['request']
        except KeyError:
            request = None

        paginator = self.get_paginator(photoset_id, request=request)

        context.update({
            'photos': paginator.page,
            'paginator': paginator,
            'photoset_id': photoset_id
        })

        return context


@register.tag(name="show_flickr_photoset")
def do_show_flickr_photoset(parser, token):
    bits = token.split_contents()
    tag = bits.pop(0)

    if len(bits) < 1:
        raise TemplateSyntaxError("'%s' takes at least one argument (title and url)" % tag)

    photoset_id = parser.compile_filter(bits.pop(0))

    kwargs = {}

    if len(bits):
        for bit in bits:
            match = kwarg_re.match(bit)
            if not match:
                raise TemplateSyntaxError("Malformed arguments to url tag")
            name, value = match.groups()
            if name:
                kwargs[name] = parser.compile_filter(value)

    template = kwargs.get('template')
    return ShowFlickrPhotosetNode(photoset_id, template=template)