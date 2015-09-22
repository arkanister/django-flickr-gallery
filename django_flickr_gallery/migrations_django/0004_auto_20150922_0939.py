# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('django_flickr_gallery', '0003_auto_20150826_1557'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60, verbose_name='nome')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='data de cria\xe7\xe3o')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categorias',
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='flickralbum',
            options={'ordering': ['title'], 'verbose_name': 'album', 'verbose_name_plural': 'albums'},
        ),
        migrations.AddField(
            model_name='flickralbum',
            name='categories',
            field=models.ManyToManyField(related_name='albums', verbose_name='categorias', to='django_flickr_gallery.Category', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='flickralbum',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 22, 12, 39, 11, 939942, tzinfo=utc), verbose_name='data de cria\xe7\xe3o', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='flickralbum',
            name='sites',
            field=models.ManyToManyField(help_text='Sites where the album will be published.', related_name='albums', verbose_name='sites', to='sites.Site'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='flickralbum',
            name='description',
            field=models.TextField(null=True, verbose_name='descri\xe7\xe3o', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='flickralbum',
            name='flickr_album_id',
            field=models.CharField(help_text='Selecione o album do flickr.', max_length=100, verbose_name='flickr album'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='flickralbum',
            name='last_sync',
            field=models.DateTimeField(help_text='Date of last sync with flickr.', verbose_name='last sync'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='flickralbum',
            name='published',
            field=models.BooleanField(default=True, verbose_name='publicado'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='flickralbum',
            name='slug',
            field=models.SlugField(help_text="Used to build the album's URL.", unique=True, max_length=130),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='flickralbum',
            name='title',
            field=models.CharField(max_length=130, verbose_name='t\xedtulo'),
            preserve_default=True,
        ),
    ]
