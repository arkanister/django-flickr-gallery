# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('django_flickr_gallery', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='flickralbum',
            options={'verbose_name': 'Album', 'verbose_name_plural': 'Album'},
        ),
        migrations.RemoveField(
            model_name='flickralbum',
            name='is_published',
        ),
        migrations.AddField(
            model_name='flickralbum',
            name='description',
            field=models.TextField(help_text='Descreva aqui este album.', null=True, verbose_name='Description', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='flickralbum',
            name='last_sync',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 10, 19, 9, 15, 270806, tzinfo=utc), help_text='Ultima sincroniza\xe7\xe3o com o flickr.', verbose_name='Last Sync'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='flickralbum',
            name='published',
            field=models.BooleanField(default=True, help_text='Desmarque para que o album n\xe3o seja visto.', verbose_name='Published'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='flickralbum',
            name='slug',
            field=models.SlugField(default='first-album', help_text='Utilizado para urls amig\xe1veis.', unique=True, max_length=130),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='flickralbum',
            name='title',
            field=models.CharField(default='First Album', help_text='T\xedtulo do Album', max_length=130, verbose_name='Title'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='flickralbum',
            name='flickr_album_id',
            field=models.CharField(help_text='Selecione o album do flickr.', unique=True, max_length=100, verbose_name='Flickr album'),
            preserve_default=True,
        ),
    ]
