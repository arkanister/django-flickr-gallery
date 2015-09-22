"""Filters for Zinnia admin"""
from django.db.models import Count
from django.utils.encoding import smart_text
from django.contrib.admin import SimpleListFilter
from django.utils.translation import ungettext_lazy
from django.utils.translation import ugettext_lazy as _

from django_flickr_gallery.models import Category


class RelatedPublishedFilter(SimpleListFilter):
    """
    Base filter for related objects to published entries.
    """
    model = None
    lookup_key = None

    def lookups(self, request, model_admin):
        """
        Return published objects with the number of entries.
        """
        active_objects = self.model.objects.all().annotate(
            count_albums=Count('albums')).order_by(
            '-count_albums', '-pk')
        for active_object in active_objects:
            yield (
                str(active_object.pk), ungettext_lazy(
                    '%(item)s (%(count)i album)',
                    '%(item)s (%(count)i albums)',
                    active_object.count_albums) % {
                    'item': smart_text(active_object),
                    'count': active_object.count_albums})

    def queryset(self, request, queryset):
        """
        Return the object's entries if a value is set.
        """
        if self.value():
            params = {self.lookup_key: self.value()}
            return queryset.filter(**params)


class CategoryListFilter(RelatedPublishedFilter):
    """
    List filter for EntryAdmin about categories
    with published entries.
    """
    model = Category
    lookup_key = 'categories__id'
    title = _('categories')
    parameter_name = 'category'
