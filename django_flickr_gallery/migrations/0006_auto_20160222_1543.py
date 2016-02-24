# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_flickr_gallery', '0005_auto_20151013_1009'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flickralbum',
            name='categories',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.RemoveField(
            model_name='flickralbum',
            name='sites',
        ),
        migrations.DeleteModel(
            name='FlickrAlbum',
        ),
    ]
