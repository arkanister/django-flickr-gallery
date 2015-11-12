from django.contrib.sitemaps import Sitemap
from django_flickr_gallery.models.album import FlickrAlbum


class FlickrAlbumSitemap(Sitemap):
    """
    Sitemap for entries.
    """
    changefreq = 'monthly'

    def items(self):
        """
        Return published entries.
        """
        return FlickrAlbum.published.all()

    def lastmod(self, obj):
        """
        Return last modification of an entry.
        """
        return obj.creation_date