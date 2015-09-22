# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_flickr_gallery', '0002_auto_20150610_1909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flickralbum',
            name='description',
            field=models.TextField(help_text='Descreva aqui este album.', null=True, verbose_name='Descri\xe7\xe3o', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='flickralbum',
            name='last_sync',
            field=models.DateTimeField(help_text='Ultima sincroniza\xe7\xe3o com o flickr.', verbose_name='\xdaltima Sincroniza\xe7\xe3o'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='flickralbum',
            name='published',
            field=models.BooleanField(default=True, help_text='Desmarque para que o album n\xe3o seja visto.', verbose_name='publicado'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='flickralbum',
            name='title',
            field=models.CharField(help_text='T\xedtulo do Album', max_length=130, verbose_name='T\xedtulo'),
            preserve_default=True,
        ),
    ]
