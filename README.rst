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

1. Install with pip or easy install (All dependencies will be installed automatically)::

    pip install django-flickr-gallery

2. Add ``django_flickr_gallery`` to your INSTALLED_APPS and all the plugins you want, setting like this::

    INSTALLED_APPS = (
        ...

        'django_flickr_gallery',
    )

3. Define migrations modules. *(Only django >= 1.7)*::

    MIGRATION_MODULES = {
        ...

        'django_flickr_gallery': 'django_flickr_gallery.migrations_django',
    }

4. Define ``FLICKR_API_KEY``, ``FLICKR_SECRET`` to Django settings. To get an api
   key and secret visit `Flickr Docs <https://www.flickr.com/services/api/>`_

5. Define ``FLICKR_USER_ID`` to Django settings. To get flickr user
   id visit `idGettr <http://idgettr.com/>`_.

6. Add ``django_flickr_gallery.urls`` to your urls with namespace='flickr-gallery'::

    urlpatterns = patterns('',
        ......
        (r'^gallery/', include('django_flickr_gallery.urls', namespace='flickr-gallery')),
        ......
    )

7. Run ``python manage.py syncdb`` or ``python manage.py migrate``.

8. Create an album into django admin in the section ``Flickr Gallery/Albums``

9. Be Happy :)

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


Photoset Tag
------------

The photoset tag is one way to render only an album at a time. It is useful to show pictures to a specific page.

To use it you need to know what the photoset id, to identify you go to `How to get photoset id <http://support.averta.net/envato/knowledgebase/find-id-photoset-flickr/>`_.::

    home.html
    {% extends 'base' %}

    {% load flickr_tags %}

    {% block content %}
        {% show_flickr_photoset 'FLICKR_PHOTOSET_ID' %}
    {% endblock content %}

Rendering with a custom template.::

    home.html
    {% extends 'base' %}

    {% load flickr_tags %}

    {% block content %}
        {% show_flickr_photoset 'FLICKR_PHOTOSET_ID' template="gallery/flickr/mytemplate.html" %}
    {% endblock content %}
