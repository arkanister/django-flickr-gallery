from django.contrib import admin, messages
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _, ungettext
from django_flickr_gallery.admin.filters import CategoryListFilter
from django_flickr_gallery.forms import FlickrCreateAlbumForm, FlickrUpdateAlbumForm
from django_flickr_gallery.utils import FlickrCallException


class FlickrAlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'last_sync', 'status')
    list_filter = (CategoryListFilter, 'status', 'last_sync')
    filter_horizontal = ['categories', 'sites']
    date_hierarchy = 'last_sync'
    form = FlickrUpdateAlbumForm

    fieldsets = (
        (None, {'fields': ('title', 'description', 'is_featured')}),
        (_("Metadata"), {'fields': ('categories', 'sites'),
                         'classes': ('collapse', 'collapse-closed')}),
        (_("Publication"), {'fields': ('slug', 'status'),
                            'classes': ('collapse', 'collapse-closed')}),
    )

    actions = ['make_published', 'make_unpublished', 'sync_album']

    def url(self, obj):
        return format_html(
            '<a href="{0}" target="_blank">{1}</a>',
            obj.get_absolute_url(), obj.get_absolute_url())

    # <editor-fold desc="actions">
    def make_published(self, request, queryset):
        queryset.update(status=self.model.PUBLISHED)
        count = queryset.count()

        message_bit = ungettext(
            "%d album was successfully marked as published.",
            "%d albums were successfully marked as published.",
            count) % count

        self.message_user(request, message_bit)

    def make_unpublished(self, request, queryset):
        queryset.update(status=self.model.HIDDEN)
        count = queryset.count()

        message_bit = ungettext(
            "%d album was successfully unmarked as published.",
            "%d albums were successfully unmarked as published.",
            count) % count

        self.message_user(request, message_bit)

    def sync_album(self, request, queryset):
        successfully_syncs = 0

        for album in queryset:
            try:
                album.sync()
                successfully_syncs += 1
            except FlickrCallException as e:
                message_bit = _("Error in sync '%s' with message '%s'.") % (
                    unicode(album),
                    e.message)

                self.message_user(request, message_bit, level=messages.ERROR)

        message_bit = ungettext(
            "%d album was successfully synced with flick.",
            "%d albums were successfully synced with flick.",
            successfully_syncs) % successfully_syncs

        self.message_user(request, message_bit)

    make_published.short_description = _("Mark selected stories as published")
    make_unpublished.short_description = _("Unmark selected stories as published")
    sync_album.short_description = _("Synchronize selected stories with flickr")
    # </editor-fold>

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            self.fieldsets = None
            return FlickrCreateAlbumForm
        else:
            return super(FlickrAlbumAdmin, self).get_form(request, obj, **kwargs)
