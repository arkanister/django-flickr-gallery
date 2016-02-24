from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_flickr_gallery.base import Photoset as FlickrPhotoset


class Photoset(models.Model):
    """
    A class to simulate a simple photoset
    object in database.
    """
    photoset_id = models.CharField(
        _('photoset id'), max_length=20,
        primary_key=True)

    creation_date = models.DateTimeField(
        _('creation date'), auto_now_add=True)

    class Meta:
        verbose_name = _('photoset')
        verbose_name_plural = _('photosets')
        ordering = ['-creation_date']

    def __get_photoset(self, force_update=False):
        if not hasattr(self, '_cached_photoset') or force_update:
            self._cached_photoset = FlickrPhotoset(id=self.photoset_id)
        return self._cached_photoset
    _photoset = property(__get_photoset)

    def get_photos_paginated(self, page=None, per_page=None):
        """
        Return paginated photos from photoset.
        :param page:
            Current page number.
        :param per_page:
            How many objects per page.
        :return: photos, paginator, page_obj.
        """
        photos, paginator, page_obj = self._photoset.getPhotos(page=page, per_page=per_page)
        return photos, paginator, page_obj

    def get_photos(self):
        """
        Returns all photos from photoset. Slowly.
        """
        photos, paginator, page_obj = self.get_photos_paginated()
        return photos

    # Slowly.
    photos = property(get_photos)

    def __unicode__(self):
        return self._photoset.title

    def _get_attr(self, key):
        return super(Photoset, self).__getattribute__(key)

    def __getattr__(self, item):
        try:
            return self._get_attr(item)
        except AttributeError:
            return getattr(self._photoset, item)
