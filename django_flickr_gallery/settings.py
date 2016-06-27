from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext as _
from django_flickr_gallery.utils.import_tools import load_class
from flickrapi.cache import SimpleCache

from django_flickr_gallery.paginator import Paginator


##############################
###### REQUIRED SETTIGS ######
##############################
try:
    API_KEY = settings.FLICKR_API_KEY
    SECRET = settings.FLICKR_SECRET
    USER_ID = settings.FLICKR_USER_ID
except AttributeError:
    raise ImproperlyConfigured(_(
        "Need to define FLICKR_API_KEY and "
        "FLICKR_SECRET and FLICKR_USER_ID"))


##############################
###### OPTIONAL SETTIGS ######
##############################
PHOTOSETS_LIST_TEMPLATE = getattr(settings, 'FLICKR_PHOTOSETS_LIST_TEMPLATE', "gallery/flickr/photoset_list.html")
PHOTOS_LIST_TEMPLATE = getattr(settings, 'FLICKR_PHOTOS_LIST_TEMPLATE', "gallery/flickr/photo_list.html")

PHOTOSET_LIST_VIEW = getattr(settings, 'FLICKR_PHOTOSET_LIST_VIEW', 'django_flickr_gallery.FlickrPhotosetListView')
PHOTO_LIST_VIEW = getattr(settings, 'FLICKR_PHOTO_LIST_VIEW', 'django_flickr_gallery.FlickrPhotosListView')

##############################
###### PAGINATOR SETTIGS #####
##############################
PAGINATOR_CLASS = Paginator

PAGE_FIELD = getattr(settings, 'FLICKR_PAGE_FIELD', "page")
PER_PAGE_FIELD = getattr(settings, 'FLICKR_PER_PAGE_FIELD', "per_page")

PHOTOS_PER_PAGE = getattr(settings, 'FLICKR_PHOTOS_PER_PAGE', 10)
PHOTOSETS_PER_PAGE = getattr(settings, 'FLICKR_PHOTOSETS_PER_PAGE', 10)

###########################
########### CACHE #########
###########################
CACHE = getattr(settings, 'FLICKR_CACHE', True)
STORE_TOKEN = getattr(settings, 'FLICKR_STORE_TOKEN', False)

CACHE_BACKEND = load_class(getattr(
    settings,
    'FLICKR_CACHE_BACKEND',
    None))