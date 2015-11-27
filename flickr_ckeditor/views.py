from django.http.response import JsonResponse
from django.views.generic.base import View

from django_flickr_gallery.utils import FlickrPhotoIterator
from django_flickr_gallery.utils import get_photosets


class CkeditorFlickrView(View):
    """
    A simple view to get flickr photos to customer.
    """
    def get(self, request, *args, **kwargs):
        page = request.GET.get('page')
        per_page = request.GET.get('per-page')

        photoset_id = request.GET.get('photoset')
        photoset_list = [(photoset['id'], photoset['title']) for photoset in get_photosets()]

        response_data = {"photosets": photoset_list, 'numOfPages': 1, 'photos': []}

        if photoset_id:
            iterator = FlickrPhotoIterator(photoset_id, page=page, per_page=per_page)

            if iterator.errors:
                response_data.update({"errors": iterator.errors})
                return JsonResponse(response_data)

            response_data['photos'] = [photo for photo in iterator.paginator.page]
            response_data['numOfPages'] = iterator.paginator.num_pages
            response_data['totalOfPhotos'] = iterator.paginator.total

        return JsonResponse(response_data)
