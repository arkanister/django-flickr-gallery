.. image:: https://travis-ci.org/arkanister/django-flickr-gallery.svg?branch=master
    :target: https://travis-ci.org/arkanister/django-flickr-gallery

.. image:: https://pypip.in/v/django-flickr-gallery/badge.png
   :target: https://pypi.python.org/pypi/django-flickr-gallery

.. image:: https://pypip.in/d/django-flickr-gallery/badge.png
   :target: https://pypi.python.org/pypi/django-flickr-gallery
   
.. image:: https://badge.waffle.io/arkanister/django-flickr-gallery.svg?label=ready&title=Ready
   :target: https://waffle.io/arkanister/django-flickr-gallery
   :alt: 'Stories in Ready' 

Django Flickr Gallery
=====================

An app to integrate django with flickr and put together a photo gallery based on flickr albums.

Installation
------------

1. Add ``django_flickr_gallery`` to your INSTALLED_APPS and all the plugins you want, setting like this::

    INSTALLED_APPS = (
        ...

        'django_flickr_gallery',
    )

2. Define migrations modules. *(Only django >= 1.7)*::

    MIGRATION_MODULES = {
        ...

        'django_flickr_gallery': 'django_flickr_gallery.migrations_django',
    }

3. Define ``FLICKR_API_KEY``, ``FLICKR_SECRET`` to Django settings. To get an api
   key and secret visit `Flickr Docs <https://www.flickr.com/services/api/>`_.

4. Define ``FLICKR_USER_ID`` to Django settings. To get flickr user
   id visit `idGettr <http://idgettr.com/>`_.

5. Run ``python manage.py migrate``.

6. Start the development server ``python manage.py runserver``
   and visit http://localhost:8000/ to be happy :).

Templates
---------

You can override the templates albums and photos, but the default template
extends the ``base.html`` template.

Use ``LIST_ALBUMS_TEMPLATE`` and ``LIST_PHOTOS_TEMPLATE`` in django settings
to change the templates that will be rendered.::

    LIST_ALBUMS_TEMPLATE = 'my_custom_albums_template.html'
    LIST_PHOTOS_TEMPLATE = 'my_custom_photos_template.html'

Photo Pagination
----------------

The application allows a setting for the paging of photos, so you can set how many
photos will be displayed per page.

Set ``FLICKR_PER_PAGE`` in django settings to change the number of photos per page.::

    FLICKR_PER_PAGE = NEW_VALUE (default=10)

