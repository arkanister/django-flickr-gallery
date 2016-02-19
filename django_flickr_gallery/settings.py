from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext as _
from flickrapi.cache import SimpleCache

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
LIST_ALBUMS_TEMPLATE = getattr(settings, 'FLICKR_LIST_ALBUMS_TEMPLATE', "gallery/flickr/album.html")
LIST_PHOTOS_TEMPLATE = getattr(settings, 'FLICKR_LIST_PHOTOS_TEMPLATE', "gallery/flickr/photos.html")

##############################
###### PAGINATOR SETTIGS #####
##############################
PAGE_FIELD = getattr(settings, 'FLICKR_PAGE_FIELD', "page")
PER_PAGE_FIELD = getattr(settings, 'FLICKR_PER_PAGE_FIELD', "per_page")

PHOTOS_PER_PAGE = getattr(settings, 'FLICKR_PHOTOS_PER_PAGE', 10)
PHOTOSETS_PER_PAGE = getattr(settings, 'FLICKR_PHOTOSETS_PER_PAGE', 10)

###########################
###### OTHER SETTIGS ######
###########################
FLICKR_STORE_TOKEN = STORE_TOKEN = False
FLICKR_CACHE = CACHE = True
FLICKR_CACHE_BACKEND = CACHE_BACKEND = SimpleCache()
