from django.db import models
from django.utils.translation import ugettext as _


class Category(models.Model):
    """
    Simple model for categorizing flickr albums.
    """

    name = models.CharField(
        _("name"), max_length=60)

    creation_date = models.DateTimeField(
        _("creation date"), auto_now_add=True)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ['name']

    def __unicode__(self):
        return self.name
