import json
from django.core.paginator import PageNotAnInteger, EmptyPage
from django.utils.translation import ugettext as _
from django_flickr_gallery import settings
from flickrapi.core import FlickrAPI
from flickrapi.exceptions import FlickrError
import six

SMALL_SQUARE = 's'
LARGE_SQUARE = 'q'
THUMBNAIL = 't'
SMALL = 'm'
SMALL_320 = 'n'
MEDIUM = '-'
MEDIUM_640 = 'z'
MEDIUM_800 = 'c'
LARGE = 'b'
LARGE_1600 = 'h'
LARGE_2048 = 'k'
ORIGINAL = 'o'

SIZES_LIST = [SMALL_SQUARE, LARGE_SQUARE, THUMBNAIL, SMALL, SMALL_320, MEDIUM, MEDIUM_640, MEDIUM_800, LARGE, LARGE_1600, LARGE_2048]


class FlickrCallException(Exception):
    """
    A exception to rises in fail to flickr call.
    """
    pass


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


def get_flickr_object():
    flickr = FlickrAPI(
        settings.API_KEY, settings.SECRET,
        cache=settings.FLICKR_CACHE,
        store_token=settings.FLICKR_STORE_TOKEN)
    flickr.cache = settings.FLICKR_CACHE_BACKEND
    return flickr


def build_flickr_call(module, method, response_format="json", quiet=False, context=None):
    """
    A builder to flickr api call.
    """
    flickr = get_flickr_object()
    context = context or {}
    call = "%s.%s" % (module, method)
    command = getattr(flickr, call)

    # add context bases
    context['format'] = response_format
    context['user_id'] = settings.USER_ID

    try:
        return command(**context)
    except FlickrError as e:
        if not quiet:
            raise FlickrError(e.message)


def call_json(module, method, quiet=False, context=None):
    messages = {
        'error': _('An error occurred while trying to make a call to the flickr.'),
    }

    response = build_flickr_call(
        module=module, method=method,
        response_format='json',
        quiet=quiet, context=context)

    if not isinstance(response, six.text_type):
        response = response.decode('utf-8')
    response = json.loads(response)

    if 'stat' in response and response['stat'] == 'fail':
        if quiet:
            return {}

        message = response['message'] if 'message' in response else messages['error']
        raise FlickrCallException(message)

    return response


def serialize_photoset(photoset):
    return {
        "id": photoset.get('id'),
        "title": parser(photoset.get('title')),
        "description": parser(photoset.get('description')),
        "primary": photoset.get('primary'),
        "count_photos": photoset.get('count_photos')
    }


def get_photosets():
    response = call_json("photosets", "getList")
    if not response:
        return None

    empty_response = {"photoset": []}
    photosets = response.get("photosets", empty_response)
    return [serialize_photoset(photoset) for photoset in photosets["photoset"]]


def get_photoset(flickr_photoset_id):
    response = call_json("photosets", "getInfo", context={"photoset_id": flickr_photoset_id})

    if not response:
        return None

    photoset = response['photoset']
    primary = photoset['primary']

    if primary is not None:
        photoset.update({'primary': get_primary(primary)})

    return serialize_photoset(photoset)


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
        elif size["label"] == "Medium 640":
            urls["url_" + MEDIUM_640] = size['source']
        elif size["label"] == "Medium 800":
            urls["url_" + MEDIUM_800] = size['source']
        elif size["label"] == "Large":
            urls["url_" + LARGE] = size['source']
        elif size["label"] == "Large 1600":
            urls["url_" + LARGE_1600] = size['source']
        elif size["label"] == "Large 2048":
            urls["url_" + LARGE_2048] = size['source']
        elif size["label"] == "Original":
            urls['url'] = size['source']

    return dict({
        "id": photo.id,
        "title": parser(photo.title),
        "description": parser(photo.description)
    }, **urls)


def get_primary(flickr_photo_id):
    context = {'photo_id': flickr_photo_id}

    photo = call_json("photos", "getInfo", context=context)
    photo_sizes = call_json("photos", "getSizes", context=context)

    if not photo or not photo_sizes:
        return None

    return serialize_primary(photo['photo'], sizes=photo_sizes["sizes"]["size"])


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


class FlickrPhotoIterator(object):
    def __init__(self, photoset_id, per_page=None, page=None, extras=None):
        self.photoset_id = photoset_id
        self.extras = extras or []
        self.per_page = per_page or settings.PER_PAGE
        self.current_page_number = page
        self.has_paginator = self.per_page is not None
        self._errors = []

    def __repr__(self):
        return "<FlickrPhotoIterator: object>"

    def __iter__(self):
        """
        Iter only in photos.
        """
        for photo in self.photos:
            yield photo

    def get_extras(self):
        return ', '.join(self.extras + ["description", "url_o"] + ["url_" + size for size in SIZES_LIST])

    def _get_paginator(self):
        if self.has_paginator and self.data:
            # get info to paginator
            params = {
                "pages": self.data.get("pages"),
                "total": self.data.get("total")
            }

            # paginator maker
            return FlickrPhotoPaginator(
                data=self.photos, per_page=self.per_page,
                page=self.current_page_number, **params)
        return None
    paginator = property(_get_paginator)

    def _flickr_call(self):
        if not hasattr(self, '_flickr_response'):
            try:
                context = {'photoset_id': self.photoset_id, 'extras': self.get_extras()}

                if self.has_paginator:
                    context['per_page'] = self.per_page
                    context['page'] = self.current_page_number

                response = call_json("photosets", "getPhotos", context=context)
                self._flickr_response = response.get("photoset")
            except FlickrError as e:
                self._flickr_response = None
                self._errors.append(e.message)
            except FlickrCallException as e:
                self._flickr_response = None
                self._errors.append(e.message)
            except AttributeError as e:
                self._flickr_response = None
                self._errors.append(e.message)
        return self._flickr_response
    data = property(_flickr_call)

    def _photos(self):
        if self.data is not None:
            photos = []
            for photo in self.data.get("photo"):
                base_url = 'https://www.flickr.com/photos/%s/%s/'
                photo_url = base_url % (self.data.get('owner'), photo.get('id'))
                photo = serialize_photo(photo)
                photo.update({
                    "absolute_url": photo_url,
                    "absolute_lightbox_url": photo_url + 'lightbox/'
                })

                photos.append(photo)

            return photos
        return None
    photos = property(_photos)

    def _get_errors(self):
        # call to update errors
        self.data
        return self._errors
    errors = property(_get_errors)


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
    def __init__(self, data, per_page=10, page=None, pages=None, total=None):
        self.data = data
        self.per_page = per_page
        self.num_pages = pages or 1
        self.total = total or 1
        self.current_page_number = int(page or 1)
        self.page = FlickrPage(self.data, self.current_page_number, self)

    def __repr__(self):
        return "<FlickrPhotoPaginator />"

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