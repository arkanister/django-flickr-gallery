from django.contrib.sitemaps import Sitemap
from django_flickr_gallery.base import Photoset
from django_flickr_gallery.utils.date import parse_unix_datetime


class FlickrAlbumSitemap(Sitemap):
    """
    Sitemap for entries.
    """
    limit = 10
    changefreq = 'monthly'

    def items(self):
        """
        Return published entries.
        """
        photosets, paginator, page = Photoset.getList()
        return photosets

    def lastmod(self, obj):
        """
        Return last modification of an entry.
        """
        return parse_unix_datetime(obj.date_update)