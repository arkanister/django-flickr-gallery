# coding: utf-8
from django.db import models
from django.core.cache import cache
from django.utils.translation import ugettext as _
from django_flickr_gallery.utils import get_photoset, AttributeDict, get_primary


class FlickrAlbum(models.Model):
    """ A model to enable flickr albums to gallery. """
    flickr_album_id = models.CharField(
        max_length=100, unique=True,
        verbose_name=_("Flikr album"),
        help_text=_("Select a flickr album."))
    is_published = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Album"
        verbose_name_plural = "Albums"

    def _photoset(self):
        cache_id = "flickr_photoset_%s" % self.flickr_album_id
        flickr_photoset = cache.get(cache_id)
        if flickr_photoset is None:
            flickr_photoset = get_photoset(self.flickr_album_id)
            cache.set(cache_id, flickr_photoset)
        return AttributeDict(flickr_photoset)
    photoset = property(_photoset)

    def _primary(self):
        cache_id = "flickr_photoset_%s_primary" % self.flickr_album_id
        flickr_photoset_primary = cache.get(cache_id)
        if flickr_photoset_primary is None:
            flickr_photoset_primary = get_primary(self.photoset.primary)
            cache.set(cache_id, flickr_photoset_primary)
        return AttributeDict(flickr_photoset_primary)
    primary = property(_primary)

    def _title(self):
        return self.photoset.title
    title = property(_title)

    def _count_photos(self):
        return self.photoset.count_photos
    count_photos = property(_count_photos)

    def __unicode__(self):
        return self.photoset.title