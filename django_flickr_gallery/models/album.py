# coding: utf-8
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import ugettext as _
from django_flickr_gallery.utils import get_photoset, AttributeDict
from django.core.cache import cache

import json


class BaseFlickrAlbum(models.Model):
    """
    Abstract core flickr album model class providing
    the fields and methods required for sync
    with flickr api albums.
    """

    flickr_album_id = models.CharField(
        max_length=100,
        verbose_name=_("flickr album"),
        help_text=_("Select a flickr album."))

    slug = models.SlugField(
        max_length=130, unique=True,
        help_text=_("Used to build the album's URL."))

    title = models.CharField(
        _("title"), max_length=130)

    description = models.TextField(
        _("description"),  null=True, blank=True)

    published = models.BooleanField(
        _("published"), default=True)

    last_sync = models.DateTimeField(
        _("last sync"),
        help_text=_("Date of last sync with flickr."))
    
    sites = models.ManyToManyField(
        Site,
        related_name='albums',
        verbose_name=_('sites'),
        help_text=_('Sites where the album will be published.'))

    creation_date = models.DateTimeField(
        _('creation date'), auto_now_add=True)

    class Meta:
        verbose_name = _("album")
        verbose_name_plural = _("albums")
        ordering = ['title']
        abstract = True

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
        super(BaseFlickrAlbum, self).save(*args, **kwargs)

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


class FickerAlbumCategories(models.Model):
    """
    Abstract model class to categorize the albums.
    """

    categories = models.ManyToManyField(
        'django_flickr_gallery.Category',
        blank=True,
        related_name='albums',
        verbose_name=_('categories'))

    class Meta:
        abstract = True


class FlickrAlbum(BaseFlickrAlbum, FickerAlbumCategories):
    """
    Final abstract album model class assembling
    all the abstract album model classes into a single one.
    """

