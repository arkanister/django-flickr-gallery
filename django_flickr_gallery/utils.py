import json
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django_flickr_gallery.settings import API_KEY, SECRET, USER_ID
from flickrapi.core import FlickrAPI
from flickrapi.exceptions import FlickrError
from django.core.cache import cache
import six


SMALL_SQUARE = 's'
LARGE_SQUARE = 'q'
THUMBNAIL = 't'
SMALL = 'm'
SMALL_320 = 'n'
MEDIUM = '-'
MEDIUM_640 = 'z'
LARGE = 'b'
ORIGINAL = 'o'

SIZES_LIST = [SMALL_SQUARE, LARGE_SQUARE, THUMBNAIL, SMALL, SMALL_320, MEDIUM, MEDIUM_640, LARGE]


class AttributeDict(dict):
    """ Simple dict like object. """
    def __getattr__(self, item, default=None):
        return self.get(item, default)

    def __setattr__(self, key, value):
        self[key] = value


def parser(value, key="_content"):
    try:
        return value.get(key)
    except AttributeError:
        return None


def build_flickr_call(module, method, response_format="json", quiet=False, **params):
    flickr = FlickrAPI(API_KEY, SECRET)
    call = "%s.%s" % (module, method)
    command = getattr(flickr, call)

    params['format'] = response_format
    params['user_id'] = USER_ID

    try:
        return command(**params)
    except FlickrError, e:
        if not quiet:
            raise FlickrError, e.message


def serialize_photoset(photoset):
    photoset = AttributeDict(photoset)
    return {
        "id": photoset.id,
        "title": parser(photoset.title),
        "description": parser(photoset.description),
        "primary": photoset.primary,
        "count_photos": photoset.count_photos
    }


def get_photosets():
    photosets = json.loads(build_flickr_call("photosets", "getList"))["photosets"]
    return [serialize_photoset(photoset) for photoset in photosets["photoset"]]


def get_photoset(flickr_photoset_id):
    photoset = build_flickr_call("photosets", "getInfo", photoset_id=flickr_photoset_id)
    return serialize_photoset(json.loads(photoset)['photoset'])


def serialize_primary(photo, sizes):
    photo = AttributeDict(photo)
    urls = {}
    for size in sizes:
        if size["label"] == "Square":
            urls["url_" + SMALL_SQUARE] = size['source']
        elif size["label"] == "Large Square":
            urls["url_" + LARGE_SQUARE] = size['source']
        elif size["label"] == "Thumbnail":
            urls["url_" + THUMBNAIL] = size['source']
        elif size["label"] == "Small":
            urls["url_" + SMALL] = size['source']
        elif size["label"] == "Small 320":
            urls["url_" + SMALL_320] = size['source']
        elif size["label"] == "Medium":
            urls["url_" + MEDIUM] = size['source']
        elif size["label"] == "Large":
            urls["url_" + LARGE] = size['source']
        elif size["label"] == "Original":
            urls['url'] = size['source']

    return dict({
        "id": photo.id,
        "title": parser(photo.title),
        "description": parser(photo.description)
    }, **urls)


def get_primary(flickr_photo_id):
    photo = build_flickr_call("photos", "getInfo", photo_id=flickr_photo_id)
    photo_sizes = build_flickr_call("photos", "getSizes", photo_id=flickr_photo_id)
    return serialize_primary(json.loads(photo)['photo'], sizes=json.loads(photo_sizes)["sizes"]["size"])


def serialize_photo(photo):
    photo = AttributeDict(photo)
    url = photo.pop("url_o")
    urls = dict([('url_' + size, photo.get('url_' + size)) for size in SIZES_LIST])
    return dict({
        "id": photo.id,
        "title": photo.title,
        "description": parser(photo.description),
        "url": url
    }, **urls)


class FlickrPage(object):

    def __init__(self, object_list, number, paginator):
        self.object_list = object_list
        self.number = number
        self.paginator = paginator

    def __repr__(self):
        return '<Page %s of %s>' % (self.number, self.paginator.num_pages)

    def __len__(self):
        return len(self.object_list)

    def __getitem__(self, index):
        if not isinstance(index, (slice,) + six.integer_types):
            raise TypeError
        # The object_list is converted to a list so that if it was a QuerySet
        # it won't be a database hit per __getitem__.
        if not isinstance(self.object_list, list):
            self.object_list = list(self.object_list)
        return self.object_list[index]

    def __iter__(self):
        for photo in self.object_list:
            yield photo

    def has_next(self):
        return self.number < self.paginator.num_pages

    def has_previous(self):
        return self.number > 1

    def has_other_pages(self):
        return self.has_previous() or self.has_next()

    def next_page_number(self):
        return self.paginator.validate_number(self.number + 1)

    def previous_page_number(self):
        return self.paginator.validate_number(self.number - 1)

    def start_index(self):
        """
        Returns the 1-based index of the first object on this page,
        relative to total objects in the paginator.
        """
        # Special case, return zero if no items.
        if self.paginator.count == 0:
            return 0
        return (self.paginator.per_page * (self.number - 1)) + 1

    def end_index(self):
        """
        Returns the 1-based index of the last object on this page,
        relative to total objects found (hits).
        """
        # Special case for the last page because there can be orphans.
        if self.number == self.paginator.num_pages:
            return self.paginator.count
        return self.number * self.paginator.per_page


class FlickrPhotoPaginator(object):
    def __init__(self, flickr_album, per_page=10, page=None, extras=None):
        self.flickr_album = flickr_album
        self.per_page = per_page
        self.current_page_number = int(page or 1)
        self.extras = extras or []
        self.page = FlickrPage(self.photos, self.current_page_number, self)

    def __repr__(self):
        return "<FlickrPhotoPaginator>"

    def get_extras(self):
        return ', '.join(self.extras + ["description", "url_o"] + ["url_" + size for size in SIZES_LIST])

    def _flickr_call(self):
        if not hasattr(self, '_flickr_response'):
            try:
                self._flickr_response = json.loads(build_flickr_call(
                    "photosets", "getPhotos",
                    photoset_id=self.flickr_album.flickr_album_id,
                    per_page=self.per_page, extras=self.get_extras(),
                    page=self.current_page_number)
                ).get("photoset")
            except FlickrError:
                self._flickr_response = None
        return self._flickr_response
    data = property(_flickr_call)

    def _photos(self):
        cache_id = "flickr_photoset_%s_photos_page_%s" % (self.flickr_album.flickr_album_id, self.current_page_number)
        flickr_photoset_photos = cache.get(cache_id)
        if flickr_photoset_photos is None:
            flickr_photoset_photos = []
            if self.data is not None:
                flickr_photoset_photos = [serialize_photo(photo) for photo in self.data.get("photo")]
            cache.set(cache_id, flickr_photoset_photos)
        return flickr_photoset_photos
    photos = property(_photos)

    def _num_pages(self):
        if self.data is not None:
            return self.data.get("pages")
        return 1
    num_pages = property(_num_pages)

    def _count(self):
        if self.data is not None:
            return self.data.get("total")
        return 0
    count = property(_count)

    def _page_range(self):
        return range(1, self.num_pages + 1)
    page_range = property(_page_range)

    def validate_number(self, number):
        """
        Validates the given 1-based page number.
        """
        try:
            number = int(number)
        except (TypeError, ValueError):
            raise PageNotAnInteger('That page number is not an integer')
        if number < 1:
            raise EmptyPage('That page number is less than 1')
        if number > self.num_pages:
            if number == 1 and self.allow_empty_first_page:
                pass
            else:
                raise EmptyPage('That page contains no results')
        return number

    def _first_page(self):
        return 1
    first_page = property(_first_page)

    def _last_page(self):
        return self.num_pages
    last_page = property(_last_page)