from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django_flickr_gallery.admin.forms import PhotosetAdminForm
from django_flickr_gallery.utils.date import parse_unix_datetime


def display_attr(func, short_description=None, boolean=False):
    def wrap(*args, **kwargs):
        return func(*args, **kwargs)

    wrap.short_description = short_description
    wrap.boolean = boolean
    return wrap


class PhotosetAdmin(admin.ModelAdmin):
    list_display = ['primary', 'title', 'description', 'count', 'last_update']
    form = PhotosetAdminForm

    primary = display_attr(
        lambda self, x: mark_safe('<img src="%s" width="48px" height="48px" />' % x.primary.small_square_url),
        short_description=_('cover'))

    title = display_attr(lambda self, x: x.title, short_description=_('title'))
    description = display_attr(lambda self, x: x.description, short_description=_('description'))
    count = display_attr(lambda self, x: x.count, short_description=_('photos'))
    last_update = display_attr(lambda self, x: parse_unix_datetime(x.date_update), short_description=_('last update'))
