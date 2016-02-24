from django.template import Library
from django_flickr_gallery.base import Photoset
from django_flickr_gallery import models
from django_flickr_gallery import settings

register = Library()


PAGE_FIELD = getattr(settings, 'PAGE_FIELD')


@register.inclusion_tag("gallery/flickr/tags/dummy.html", takes_context=True)
def get_photos_by_photoset(context, photoset_id, page=None, per_page=None,
                           template_name="gallery/flickr/tags/photoset.html"):
    """
    Get photos by photoset_id. Allow paginator.
    :param context:
        Context object.
    :param photoset_id:
        Photoset id to get a photoset.
    :param page:
        Current page number.
    :param per_page:
        How many objects per page.
    :param template_name:
        Template to render tag.
    :return: context object.
    """
    request = context['request']

    # get page number
    if per_page is not None:
        page = page or request.GET.get(PAGE_FIELD, None)

    photoset = Photoset(id=photoset_id)
    photos, paginator, page_obj = photoset.getPhotos(page=page, per_page=per_page)
    is_paginated = paginator is not None and page_obj is not None

    context = {
        'photoset': photoset,
        'photos': photos,
        'object_list': photos,
        'template': template_name
    }

    if is_paginated:
        context.update({
            'is_paginated': True,
            'paginator': paginator,
            'page_obj': page_obj
        })

    return context


@register.inclusion_tag("gallery/flickr/tags/dummy.html", takes_context=True)
def get_featured_photosets(context, count=3, count_photos=10,
                           template_name="gallery/flickr/tags/featured.html"):
    """
    Get from database featured photosets. Not allow paginator.
    :param context:
        Context object.
    :param count:
        Counts photosets to get.
    :param count_photos:
        How many photos limit by photosets.
    :param template_name:
        Template to render tag.
    :return: context object.

    Usage:
        >>> {% load flickr_tags %}
        >>> {% get_featured_photosets count=1 count_photos=10 template_name="gallery/flickr/another_template.html" %}
    """
    object_list = []

    for photoset in models.Photoset.objects.all()[:count]:
        photos, paginator, page_obj = photoset.get_photos_paginated(page=1, per_page=count_photos)
        object_list.append((photoset, photos))

    context.update({
        'featured': object_list,
        'template': template_name
    })
    return context


@register.inclusion_tag('gallery/flickr/tags/dummy.html', name='paginator', takes_context=True)
def do_paginator(context, page_obj, template_name='gallery/flickr/tags/pagination.html'):
    """
    Simple paginator to shows pages in list with specific template.
    :param context: Base view context.
    :param page_obj: page object.
    :param template_name: template name to render this.
    :return: Context object
    """
    request = context.get('request')

    return {
        'paginator': page_obj.paginator,
        'page_obj': page_obj,
        'request': request,
        'template': template_name
    }
