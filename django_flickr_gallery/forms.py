from django import forms
from django_flickr_gallery.models import FlickrAlbum
from django_flickr_gallery.utils import get_photosets
from flickrapi.exceptions import FlickrError


class FlickrAlbumForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(FlickrAlbumForm, self).__init__(*args, **kwargs)
        choices = (("", "----------"),)
        try:
            choices += tuple([(photoset['id'], photoset['title']) for photoset in get_photosets()])
        except FlickrError, e:
            print e.message

        # set choices with flickr albums
        self.fields['flickr_album_id'].widget = forms.Select(choices=choices)

    class Meta:
        model = FlickrAlbum