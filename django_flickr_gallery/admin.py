from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import ugettext as _
from django_flickr_gallery.forms import FlickrCreateAlbumForm, FlickrUpdateAlbumForm
from django_flickr_gallery.models import FlickrAlbum

class FlickrAlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'last_sync', 'published')
    list_filter = ('published', 'last_sync')
    form = FlickrUpdateAlbumForm
    prepopulated_fields = {"slug": ('title',)}

    actions = ['make_published', 'make_unpublished', 'sync_album']

    def url(self, obj):
        return format_html(
            '<a href="{0}" target="_blank">{1}</a>',
            obj.get_absolute_url(), obj.get_absolute_url())

    # <editor-fold desc="actions">
    def make_published(self, request, queryset):
        queryset.update(published=True)

        if queryset.count() == 1:
            message_bit = "1 story was successfully marked as published."
        else:
            message_bit = "%s stories were successfully marked as published." % queryset.count()
        self.message_user(request, message_bit)

    def make_unpublished(self, request, queryset):
        queryset.update(published=False)

        if queryset.count() == 1:
            message_bit = "1 story was successfully unmarked as published."
        else:
            message_bit = "%s stories were successfully unmarked as published." % queryset.count()
        self.message_user(request, message_bit)

    def sync_album(self, request, queryset):
        for album in queryset:
            album.sync()

        if queryset.count() == 1:
            message_bit = "1 story was successfully synced with flick."
        else:
            message_bit = "%s stories were successfully synced with flick." % queryset.count()
        self.message_user(request, message_bit)

    make_published.short_description = _("Mark selected stories as published")
    make_unpublished.short_description = _("Unmark selected stories as published")
    sync_album.short_description = _("Synchronize selected stories with flickr")
    # </editor-fold>

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            return FlickrCreateAlbumForm
        else:
            return super(FlickrAlbumAdmin, self).get_form(request, obj, **kwargs)


admin.site.register(FlickrAlbum, FlickrAlbumAdmin)