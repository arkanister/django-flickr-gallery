# coding: utf-8
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import ugettext as _
from django_flickr_gallery.utils import get_photoset, AttributeDict
from django.core.cache import cache

import json

class FlickrAlbum(models.Model):
    """ A model to enable flickr albums to gallery. """
    flickr_album_id = models.CharField(
        max_length=100, unique=True,
        verbose_name=_("Flickr album"),
        help_text=_("Select a flickr album."))

    slug = models.SlugField(
        max_length=130, unique=True,
        help_text=_("Used to generate friendly urls."))

    title = models.CharField(
        _("Title"), max_length=130,
        help_text=_("Album title."))

    description = models.TextField(
        _("Description"),  null=True, blank=True,
        help_text=_("Describe this album here."))

    published = models.BooleanField(
        _("Published"), default=True,
        help_text=_("Unmark if the album can not be visible."))

    last_sync = models.DateTimeField(
        _("Last Sync"),
        help_text=_("The last sync with flickr api."))

    class Meta:
        verbose_name = _("Album")
        verbose_name_plural = _("Album")

    @property
    def photoset(self):
        photoset_data = cache.get("flickr_photoset_%s" % self.flickr_album_id)
        if photoset_data is None:
            photoset_data = get_photoset(self.flickr_album_id)
            cache.set("flickr_photoset_%s" % self.slug, json.dumps(photoset_data), 60 * 15)
        else:
            photoset_data = json.loads(photoset_data)
        return AttributeDict(photoset_data)

    @property
    def count_photos(self):
        return self.photoset.count_photos

    @property
    def cover(self):
        return self.photoset.primary

    def save(self, *args, **kwargs):
        if not self.pk:
            # the first sync
            self.sync(commit=False)
        super(FlickrAlbum, self).save(*args, **kwargs)

    def sync(self, commit=True):
        self.title = self.photoset.title
        self.slug = slugify(self.title)
        self.description = self.photoset.description
        self.last_sync = timezone.now()

        # force commit changes
        if commit:
            self.save()

    def get_absolute_url(self):
        return reverse('gallery-photos', kwargs={"slug": self.slug})

    def __unicode__(self):
        return self.title