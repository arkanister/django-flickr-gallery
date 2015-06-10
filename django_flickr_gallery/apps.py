from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class DjangoFlickrGalleryAppConfig(AppConfig):
    name = 'django_flickr_gallery'
    verbose_name = _("Flickr Gallery")