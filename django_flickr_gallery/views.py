# coding: utf-8
from django.views.generic.base import TemplateView
from django_flickr_gallery import settings
from django_flickr_gallery.base import Photoset


class PaginatedMixin(object):
    paginate_by = None
    context_object_name = None
    page_kwarg = 'page'

    def get_context_object_name(self):
        """
        Get the name of the item to be used in the context.
        """
        if self.context_object_name:
            return self.context_object_name
        else:
            return None

    def paginate(self, page_number, page_size):
        """
        Paginate the queryset, if needed.
        """
        raise NotImplementedError

    def get_paginate_by(self):
        """
        Get the number of items to paginate by, or ``None`` for no pagination.
        """
        return self.paginate_by

    def get_page_number(self):
        """
        Get the number of current page to pagination.
        """
        return self.request.GET.get(self.page_kwarg)

    def get_context_data(self, **kwargs):
        """
        Get the context for this view.
        """
        page_size = self.get_paginate_by()
        page_number = self.get_page_number()
        context_object_name = self.get_context_object_name()
        object_list, paginator, page = self.paginate(page_number, page_size)

        is_paginated = page_size and paginator is not None and page is not None

        if is_paginated:
            context = {
                'paginator': paginator,
                'page_obj': page,
                'is_paginated': is_paginated,
                'object_list': object_list
            }
        else:
            context = {
                'paginator': None,
                'page_obj': None,
                'is_paginated': is_paginated,
                'object_list': object_list
            }
        if context_object_name is not None:
            context[context_object_name] = object_list

        context.update(kwargs)

        print context
        return super(PaginatedMixin, self).get_context_data(**context)


class FlickrAlbumListView(PaginatedMixin, TemplateView):
    template_name = settings.LIST_ALBUMS_TEMPLATE
    paginate_by = getattr(settings, 'PHOTOSETS_PER_PAGE')
    page_field = getattr(settings, 'PAGE_FIELD')
    per_page_field = getattr(settings, 'PER_PAGE_FIELD')
    context_object_name = 'photosets'

    def paginate(self, page_number, page_size):
        photosets, paginator, page = Photoset.getList(page=page_number, per_page=page_size)
        return photosets, paginator, page


class FlickrAlbumPhotoListView(PaginatedMixin, TemplateView):
    template_name = settings.LIST_PHOTOS_TEMPLATE
    paginate_by = getattr(settings, 'PHOTOS_PER_PAGE')
    page_kwarg = getattr(settings, 'PAGE_FIELD')
    per_page_field = getattr(settings, 'PER_PAGE_FIELD')
    context_object_name = 'photos'
    photoset = None

    def paginate(self, page_number, page_size):
        self.photoset = Photoset(id=self.kwargs.get('photoset_id'))
        photos, paginator, page = self.photoset.getPhotos(page=page_number, per_page=page_size)
        return photos, paginator, page

    def get_context_data(self, **kwargs):
        context = super(FlickrAlbumPhotoListView, self).get_context_data(**kwargs)
        context['photoset'] = self.photoset
        return context
