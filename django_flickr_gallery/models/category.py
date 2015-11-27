from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
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

    def __str__(self):
        return self.name
