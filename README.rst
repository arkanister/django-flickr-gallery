.. image:: https://badge.fury.io/py/django-flickr-gallery.svg
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

6. Add ``django_flickr_gallery.urls`` to your urls::

    urlpatterns = patterns('',
        ...

        (r'^gallery/', include('django_flickr_gallery.urls'),
    )

7. Run ``python manage.py syncdb`` or ``python manage.py migrate``.

8. Create an album into django admin in the section ``Flickr Gallery/Albums``

9. Be Happy :)

Templates
---------

You can override the templates albums and photos, but the default template
extends the ``base.html`` template.

Use ``FLICKR_LIST_ALBUMS_TEMPLATE`` and ``FLICKR_LIST_PHOTOS_TEMPLATE`` in django settings
to change the templates that will be rendered.::

    FLICKR_LIST_ALBUMS_TEMPLATE = 'my_custom_albums_template.html'
    FLICKR_LIST_PHOTOS_TEMPLATE = 'my_custom_photos_template.html'

Photo Pagination
----------------

The application allows a setting for the paging of photos, so you can set how many
photos will be displayed per page.

Set ``FLICKR_PER_PAGE`` in django settings to change the number of photos per page.::

    FLICKR_PER_PAGE = NEW_VALUE (default=10)

Set ``FLICKR_PER_PAGE`` as None to disable pagination.

Photoset Tag
------------

The photoset tag is one way to render only an album at a time. It is useful to show pictures to a specific page.

To use it you need to know what the photoset id, to identify you go to `How to get photoset id <http://support.averta.net/envato/knowledgebase/find-id-photoset-flickr/>`_.::

    home.html
    {% extends 'base.html' %}

    {% load flickr_tags %}

    {% block content %}
        {% show_flickr_photoset 'FLICKR_PHOTOSET_ID' %}
    {% endblock content %}

Rendering with a custom template.::

    home.html
    {% extends 'base.html' %}

    {% load flickr_tags %}

    {% block content %}
        {% show_flickr_photoset 'FLICKR_PHOTOSET_ID' template="gallery/flickr/mytemplate.html" %}
    {% endblock content %}

CKEDITOR plugin
---------------

The ``flickr_ckeditor`` is a ckeditor plugin to get flickr photos in django ckeditor.

Usage

1. Add ``flickr_ckeditor`` to your INSTALLED_APPS and all the plugins you want, setting like this::

    INSTALLED_APPS = (
        ...

        'flickr_ckeditor',
    )

2. Add url setting in ``urls.py``, it needs to be just that way::

    urlpatterns = patterns(''
        ...
        url(r'^ckeditor/flickr/', include('flickr_ckeditor.urls')),
        ...
    )

3. Add plugin in ckeditor, in ``extraPlugins`` and ``Flickr`` in toolbar::

    CKEDITOR_CONFIGS = {
        'default': {
            'toolbar_MyToolbar': [
                ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord'],
                ['Undo', 'Redo'],
                ['Scayt'],
                ['Link', 'Unlink', 'Anchor'],
                ['Image', 'Flickr', 'Table', 'HorizontalRule', 'SpecialChar'],
                ['Source'],
                ['Maximize', 'ReadMore'],
                '/',
                ['Bold', 'Italic', 'Underline', 'Strike',
                 'Subscript', 'Superscript', '-', 'RemoveFormat'],
                ['NumberedList', 'BulletedList', '-',
                 'Outdent', 'Indent', '-', 'Blockquote'],
                ['Styles', 'Format'],
            ],
            'extraPlugins': 'flickr',
            'toolbar': 'MyToolbar',
        },
    }

4. Be Happy :)

Note that the precision configuration variables are set correctly in django settings.

Contributors
------------

`arkanister <https://github.com/arkanister/>`_

`sikmir <https://github.com/sikmir/>`_