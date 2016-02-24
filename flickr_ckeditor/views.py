from django.http.response import JsonResponse
from django.views.generic.base import View

from django_flickr_gallery.base import Photoset


class CkeditorFlickrView(View):
    """
    A simple view to get flickr photos to customer.
    """
    def get(self, request, *args, **kwargs):
        num_page = request.GET.get('page')
        per_page = request.GET.get('per-page')

        photosets, paginator, page = Photoset.getList()

        photoset_id = request.GET.get('photoset')
        photoset_list = [(photoset.id, photoset.title) for photoset in photosets]

        response_data = {"photosets": photoset_list, 'numOfPages': 1, 'photos': []}

        if photoset_id:
            photoset = list(filter(lambda x: x.id == photoset_id, photosets))

            if len(photoset):
                photoset = photoset.pop()
                photos, paginator, page = photoset.getPhotos(page=num_page, per_page=per_page)

                response_data['photos'] = [{
                    "id": photo.id,
                    "title": photo.title,
                    "large_square_url": photo.large_square_url,
                    "medium_url": photo.medium_url,
                    "url": photo.url
                } for photo in page]

                response_data['numOfPages'] = paginator.num_pages
                response_data['totalOfPhotos'] = paginator.total

        return JsonResponse(response_data)
