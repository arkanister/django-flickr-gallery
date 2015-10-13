from django.db import models


class AlbumFeaturedManager(models.Manager):
    def get_queryset(self):
        queryset = super(AlbumFeaturedManager, self).get_queryset()
        queryset.filter(status=self.model.PUBLISHED, is_featured=True)
        return queryset


class AlbumPublishedManager(models.Manager):
    def get_queryset(self):
        queryset = super(AlbumPublishedManager, self).get_queryset()
        queryset.filter(status=self.model.PUBLISHED)
        return queryset
