from django import forms
from django_flickr_gallery.models import FlickrAlbum
from django_flickr_gallery.utils import get_photosets
from flickrapi.exceptions import FlickrError


class FlickrCreateAlbumForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FlickrCreateAlbumForm, self).__init__(*args, **kwargs)
        choices = (("", "----------"),)
        try:
            existing_album = [album.flickr_album_id for album in FlickrAlbum.objects.all()]
            photosets = [(photoset['id'], photoset['title']) for photoset in get_photosets()]
            photosets = filter(lambda x: x[0] not in existing_album, photosets)
            choices += tuple(photosets)
        except FlickrError as e:
            print(e.message)

        # set choices with flickr albums
        self.fields['flickr_album_id'].widget = forms.Select(choices=choices)

    class Meta:
        model = FlickrAlbum
        fields = ['flickr_album_id', 'sites']


class FlickrUpdateAlbumForm(forms.ModelForm):
    class Meta:
        model = FlickrAlbum
        exclude = ['flickr_album_id', 'last_sync']
