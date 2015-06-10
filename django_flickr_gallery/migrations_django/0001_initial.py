# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FlickrAlbum',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('flickr_album_id', models.CharField(help_text='Select a flickr album.', unique=True, max_length=100, verbose_name='Flikr album')),
                ('is_published', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Album',
                'verbose_name_plural': 'Albums',
            },
            bases=(models.Model,),
        ),
    ]
