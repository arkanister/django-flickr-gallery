# coding: utf-8
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from django_flickr_gallery.models.managers import AlbumFeaturedManager
from django_flickr_gallery.models.managers import AlbumPublishedManager

from django_flickr_gallery.utils import get_photoset, AttributeDict


@python_2_unicode_compatible
class BaseFlickrAlbum(models.Model):
    """
    Abstract core flickr album model class providing
    the fields and methods required for sync
    with flickr api albums.
    """
    HIDDEN = 0
    PUBLISHED = 1
    STATUS = ((HIDDEN, _("Hidden")), (PUBLISHED, _("Published")))

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

    last_sync = models.DateTimeField(
        _("last sync"),
        help_text=_("Date of last sync with flickr."))

    status = models.IntegerField(
        _("status"), default=PUBLISHED,
        choices=STATUS)

    creation_date = models.DateTimeField(
        _('creation date'), auto_now_add=True)

    objects = models.Manager()
    published = AlbumPublishedManager()

    class Meta:
        verbose_name = _("album")
        verbose_name_plural = _("albums")
        ordering = ['title']
        abstract = True

    @property
    def photoset(self):
        if not hasattr(self, 'photoset_data'):
            self.photoset_data = AttributeDict(get_photoset(self.flickr_album_id))
        return self.photoset_data

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

    def __str__(self):
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


class FlickrAlbumFeatured(models.Model):
    """
    Enable support to featured albums.
    """

    is_featured = models.BooleanField(
        _("featured"), default=False)

    featured = AlbumFeaturedManager()

    class Meta:
        abstract = True


class FlickrAlbumSites(models.Model):

    sites = models.ManyToManyField(
        Site,
        related_name='albums',
        verbose_name=_('sites'),
        help_text=_('Sites where the album will be published.'))

    class Meta:
        abstract = True


class FlickrAlbum(BaseFlickrAlbum, FickerAlbumCategories,
                  FlickrAlbumFeatured, FlickrAlbumSites):
    """
    Final abstract album model class assembling
    all the abstract album model classes into a single one.
    """

