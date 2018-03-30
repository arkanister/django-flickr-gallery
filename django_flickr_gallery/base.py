from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.http import Http404
from django.utils.translation import ugettext as _
from django_flickr_gallery import settings
from django_flickr_gallery.shortcuts import get_paginator

from flickrapi import FlickrAPI as BaseFlickrAPI, FlickrError


API_KEY = getattr(settings, 'API_KEY')
SECRET = getattr(settings, 'SECRET')
CACHE = getattr(settings, 'CACHE')
CACHE_BACKEND = getattr(settings, 'CACHE_BACKEND')
STORE_TOKEN = getattr(settings, 'STORE_TOKEN')
USER_ID = getattr(settings, 'USER_ID')


class FlickrAPI(BaseFlickrAPI):
    """
    Apply singleton pattern to FlickrAPI.
    Need only one instance of FlickrApi in this app,
    because is about only one settings.
    """
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_flickr_api_instance'):
            cls._flickr_api_instance = BaseFlickrAPI(*args, **kwargs)
        return cls._flickr_api_instance

    @staticmethod
    def construct():
        """
        Get FlickrAPI object.
        :return:
        """
        _flickr = FlickrAPI(
            API_KEY, SECRET,
            store_token=STORE_TOKEN,
            cache=CACHE)

        _flickr.cache = CACHE_BACKEND
        return _flickr


def _get_direct_url(size):
    def __get_direct_url(self):
        return "http://farm%s.static.flickr.com/%s/%s_%s_%s.jpg" % \
            (self.farm, self.server, self.id, self.secret, size)
    return __get_direct_url


class Photo(object):
    """Represents a Flickr Photo."""
    def __init__(self, id, secret=None, server=None, farm=None,
                 tags=None, title=None,
                 description=None, data=None):
        """Must specify id, rest is optional."""
        self.id = id
        self._data = data

        if data is not None:
            secret = data.get('secret', secret)
            server = data.get('server', server)
            farm = data.get('farm', farm)
            title = data.get('title', title)
            description = data.get('description', description)

        self.__title = title
        self.__description = description
        self.secret = secret
        self.server = server
        self.farm = farm
        self.tags = tags

    @staticmethod
    def getInfo(id):
        pass

    @staticmethod
    def getList(id, photoset_id):
        pass

    def _val(self, key):
        return super(Photoset, self).__getattribute__(key)

    def __getattr__(self, item):
        try:
            val = self._val(item)

        except AttributeError as e:
            val = self._data.get(item, None)

            if val is None:
                raise AttributeError(e)
        return val

    def __get_title(self):
        if self.__title is None:
            return
        elif isinstance(self.__title, (str, bytes)):
            return self.__title
        elif isinstance(self.__title, dict):
            self.__title = self.__title.get('_content', None)
        return self.__title
    title = property(__get_title)

    def __get_description(self):
        if self.__description is None:
            return
        elif isinstance(self.__description, (str, bytes)):
            return self.__description
        elif isinstance(self.__description, dict):
            self.__description = self.__description.get('_content', None)
        return self.__description
    description = property(__get_description)

    def __url(self):
        return 'https://www.flickr.com/photos/%s/%s/' % (USER_ID, self.id)
    url = property(__url)

    def __repr__(self):
        return '<Flickr Photo: %s>' % self.id

    thumbnail_url = property(_get_direct_url('t'))
    small_square_url = property(_get_direct_url('s'))
    large_square_url = property(_get_direct_url('q'))
    small_url = property(_get_direct_url('m'))
    small_320_url = property(_get_direct_url('n'))
    medium_url = property(_get_direct_url('z'))
    medium_800_url = property(_get_direct_url('c'))
    large_url = property(_get_direct_url('b'))
    large_1600_url = property(_get_direct_url('h'))


class Photoset(object):
    """A Flickr photoset.

    If constructed with just an ID, the rest of the data about the Photoset is
    fetched from the API.
    """
    id = None

    def __init__(self, id, title=None, primary=None, photos=0, description='', data=None):
        self.id = id
        self._data = data or self._get_photoset()

        if self._data is not None:
            title = self._data['title']
            description = self._data['description']
            primary = Photo(self._data['primary'], data={
                'farm': self._data['farm'],
                'server': self._data['server'],
                'secret': self._data['secret'],
            })
            photos = self._data['photos']

        self.primary = primary
        self.__title = title
        self.__description = description
        self.count = photos

    def __get_title(self):
        if self.__title is None:
            return
        elif isinstance(self.__title, (str, bytes)):
            return self.__title
        elif isinstance(self.__title, dict):
            self.__title = self.__title.get('_content', None)
        return self.__title
    title = property(__get_title)

    def __get_description(self):
        if self.__description is None:
            return
        elif isinstance(self.__description, (str, bytes)):
            return self.__description
        elif isinstance(self.__description, dict):
            self.__description = self.__description.get('_content', None)
        return self.__description
    description = property(__get_description)

    def _val(self, key):
        return super(Photoset, self).__getattribute__(key)

    def __getattr__(self, item):
        try:
            val = self._val(item)

        except AttributeError as e:
            val = self._data.get(item, None)

            if val is None:
                raise AttributeError(e)
        return val

    def __len__(self):
        return self.__count

    def __repr__(self):
        return '<Flickr Photoset: %s>' % self.id

    def _get_photoset(self, user_id=USER_ID, **params):
        """
        Request a single photoset info.
        :param photoset_id:
            The ID of the photoset to fetch information for.
        :param user_id:
            The user_id here is the owner of the set passed in photoset_id.
            This is optional, but passing this gives better performance.
        :param params:
            Extra params to request in flickr api.
        :return:
        """
        flickr = FlickrAPI.construct()

        try:
            params.update({
                'user_id': user_id,
                'photoset_id': self.id,
                'format': "json"
            })

            response = flickr.photosets.getInfo(**params)

            if isinstance(response, (str, bytes)):
                response = flickr.parse_json(response)

            return response.get('photoset')
        except FlickrError as e:
            if e.code == 1:
                raise Http404(_("Photoset not found."))
            elif e.code == 2:
                raise Http404(_("User not found."))
            raise FlickrError(e.message)

    @staticmethod
    def getList(user_id=USER_ID, page=None, per_page=None, **params):
        """
        Get list of photosets. Allow paginator
        :param user_id:
            The NSID of the user to get a photoset list for.
            If none is specified, the calling user is assumed.
        :param page:
            The page of results to return. If this argument is omitted, it
            defaults to 1.
        :param per_page:
            Number of photos to return per page. If this argument is
            omitted, it defaults to 500. The maximum allowed value is 500.
        :param params:
            Extra params to request in flickr api.
        :return: object_list, paginator and page_obj
        """
        flickr = FlickrAPI.construct()

        try:
            params.update({
                'user_id': user_id,
                'format': 'json',
                'per_page': per_page,
                'page': page or 1
            })

            response = flickr.photosets.getList(**params)

            if isinstance(response, (str, bytes)):
                response = flickr.parse_json(response)

            def parse_reponse(response):
                _photosets = response.get('photosets', None)

                if not _photosets:
                    return [None, None, None, None, None]

                return (
                    _photosets['photoset'],
                    _photosets['total'],
                    _photosets['page'],
                    _photosets['perpage'],
                    _photosets['pages']
                )

            photosets, total, page, per_page, pages = parse_reponse(response)
            photosets = [Photoset(id=photoset['id'], data=photoset) for photoset in photosets]
            paginator, page_obj = None, None

            if per_page is not None:
                paginator, page_obj = get_paginator(
                    photosets, page=page, per_page=per_page,
                    pages=pages, total=total)

            return photosets, paginator, page_obj

        except FlickrError as e:
            if e.code == 1:
                raise Http404(_("Photosets not found."))

    def getPhotos(self, user_id=USER_ID, page=None, per_page=None, privacy_filter=1, **params):
        """
        Get photos from flickr photosets. Allow paginator.
        :param user_id:
            The user_id here is the owner of the set passed in photoset_id.
            This is optional, but passing this gives better performance.
        :param page:
            The page of results to return. If this argument is omitted, it
            defaults to 1.
        :param per_page:
            Number of photos to return per page. If this argument is
            omitted, it defaults to 500. The maximum allowed value is 500.
        :param privacy_filter:
            Return photos only matching a certain privacy level. This only
            applies when making an authenticated call to view a photoset
            you own. Valid values are:

            1 public photos
            2 private photos visible to friends
            3 private photos visible to family
            4 private photos visible to friends & family
            5 completely private photos
        :param params:
            Extra params to request in flickr api.
        :return: object_list, paginator and page_obj
        """
        flickr = FlickrAPI.construct()

        try:
            params.update({
                'photoset_id': self.id,
                'user_id': user_id,
                'format': 'json',
                'per_page': per_page,
                'page': page or 1,
                'privacy_filter': privacy_filter,
                'media': 'photos',
                'extras': 'description'
            })

            response = flickr.photosets.getPhotos(**params)

            if isinstance(response, (str, bytes)):
                response = flickr.parse_json(response)

            def parse_reponse(response):
                _photoset = response.get('photoset', None)

                if not _photoset:
                    return [None, None, None, None, None]

                return [
                    _photoset['photo'],
                    _photoset['total'],
                    _photoset['page'],
                    _photoset['perpage'],
                    _photoset['pages']
                ]

            photos, total, page, per_page, pages = parse_reponse(response)
            paginator, page_obj = None, None

            if photos is not None:
                photos = [Photo(photo['id'], data=photo) for photo in photos]

            if per_page is not None:
                paginator, page_obj = get_paginator(
                    photos, page=page, per_page=per_page,
                    pages=pages, total=total)

            return photos, paginator, page_obj
        except FlickrError as e:
            if e.code == 1:
                raise Http404(_("Photoset %s not found.") % self.id)

    def __url(self):
        return 'https://www.flickr.com/photos/%s/sets/%s/' % (USER_ID, self.id)
    url = property(__url)

    def get_absolute_url(self):
        return reverse('flickr-photo-list', kwargs={"photoset_id": self.id})
