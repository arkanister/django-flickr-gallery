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

3. Define ``FLICKR_API_KEY``, ``FLICKR_SECRET`` to Django settings. To get an api
   key and secret visit `Flickr Docs <https://www.flickr.com/services/api/>`_

4. Define ``FLICKR_USER_ID`` to Django settings. To get flickr user
   id visit `idGettr <http://idgettr.com/>`_.

5. Add ``django_flickr_gallery.urls`` to your urls::

    urlpatterns = patterns('',
        ...

        (r'^gallery/', include('django_flickr_gallery.urls'),
    )

6. Run ``python manage.py syncdb`` or ``python manage.py migrate``.

7. Create an album into django admin in the section ``Flickr Gallery/Albums``

8. Be Happy :)

Templates
---------

You can override the templates albums and photos, but the default template
extends the ``base.html`` template.

Use ``FLICKR_PHOTOSETS_LIST_TEMPLATE`` and ``FLICKR_PHOTOS_LIST_TEMPLATE`` in django settings
to change the templates that will be rendered.::

    FLICKR_PHOTOSETS_LIST_TEMPLATE = 'my_custom_albums_template.html'
    FLICKR_PHOTOS_LIST_TEMPLATE = 'my_custom_photos_template.html'

Photosets Pagination
--------------------

The application allows a setting for the paging of photos, so you can set how many
photos will be displayed per page.

Set ``FLICKR_PHOTOSETS_PER_PAGE`` in django settings to change the number of photos per page.::

    FLICKR_PHOTOSETS_PER_PAGE = NEW_VALUE (default=10)

Set ``FLICKR_PHOTOSETS_PER_PAGE`` as None to disable pagination.

Photo Pagination
----------------

The application allows a setting for the paging of photos, so you can set how many
photos will be displayed per page.

Set ``FLICKR_PHOTOS_PER_PAGE`` in django settings to change the number of photos per page.::

    FLICKR_PHOTOS_PER_PAGE = NEW_VALUE (default=10)

Set ``FLICKR_PHOTOS_PER_PAGE`` as None to disable pagination.


Template Tags
-------------

Available tags

*get_photos_by_photoset*

The photoset tag is one way to render only an album at a time. It is useful to show pictures to a specific page.

To use it you need to know what the photoset id, to identify you go to `How to get photoset id <http://support.averta.net/envato/knowledgebase/find-id-photoset-flickr/>`_.::

    home.html
    {% extends 'base.html' %}

    {% load flickr_tags %}

    {% block content %}
        {% get_photos_by_photoset 'FLICKR_PHOTOSET_ID' template_name="gallery/flickr/mytemplate.html" %}
    {% endblock content %}


*get_featured_photosets*

Can show some photosets with some pictures to display, like as summary of the each photoset::

    home.html
    {% extends 'base.html' %}

    {% load flickr_tags %}

    {% block content %}
        {% get_featured_photosets count=3 count_photos=10 template_name="gallery/flickr/mytemplate.html" %}
    {% endblock content %}

*paginator*

Render the paginator of photosets or photos, required ``page_obj``::

    home.html
    {% extends 'base.html' %}

    {% load flickr_tags %}

    {% block content %}
        {% paginator page_obj %}
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