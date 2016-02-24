from django import forms
from django_flickr_gallery.base import Photoset
from django_flickr_gallery.models import Photoset as PhotosetModel


BLANK_OPTION = ("", "----------")


def photosets_as_choices(blank_option=BLANK_OPTION):
    choices = (blank_option,)
    exclude = [photoset.photoset_id for photoset in PhotosetModel.objects.all()]

    photosets, paginator, page_obj = Photoset.getList()
    photosets = [(photoset.id, photoset.title) for photoset in photosets if not photoset.id in exclude]
    choices += tuple(photosets)
    return choices


class PhotosetAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PhotosetAdminForm, self).__init__(*args, **kwargs)

        # set choices with flickr albums
        self.fields['photoset_id'].widget = forms.Select(choices=photosets_as_choices())

    class Meta:
        model = PhotosetModel
        fields = '__all__'
