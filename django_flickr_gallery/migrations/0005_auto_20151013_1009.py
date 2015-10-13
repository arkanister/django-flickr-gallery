# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def migrate_status(apps, schema_editor):
    FlickrAlbum = apps.get_model("django_flickr_gallery", "FlickrAlbum")
    queryset = FlickrAlbum.objects.all()

    # published
    migrate_published = queryset.filter(published=True)
    migrate_published.update(status=1)

    # hidden
    migrate_hidden = queryset.filter(published=False)
    migrate_hidden.update(status=0)


class Migration(migrations.Migration):

    dependencies = [
        ('django_flickr_gallery', '0004_auto_20150922_0939'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['name'], 'verbose_name': 'Categoria', 'verbose_name_plural': 'Categorias'},
        ),
        migrations.AlterModelOptions(
            name='flickralbum',
            options={'ordering': ['title'], 'verbose_name': 'album', 'verbose_name_plural': 'Albuns'},
        ),
        migrations.AddField(
            model_name='flickralbum',
            name='status',
            field=models.IntegerField(default=1, verbose_name='status', choices=[(0, 'Oculto'), (1, 'Publicado')]),
            preserve_default=True,
        ),
        migrations.RunPython(migrate_status),  # run migrations by status
        migrations.RemoveField(
            model_name='flickralbum',
            name='published',
        ),
        migrations.AddField(
            model_name='flickralbum',
            name='is_featured',
            field=models.BooleanField(default=True, verbose_name='featured'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='flickralbum',
            name='flickr_album_id',
            field=models.CharField(help_text='Selecione o album do flickr.', max_length=100, verbose_name='album do flickr.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='flickralbum',
            name='last_sync',
            field=models.DateTimeField(help_text='Data da \xfaltima sincroniza\xe7\xe3o com o flickr.', verbose_name='\xdaltima Sincroniza\xe7\xe3o'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='flickralbum',
            name='sites',
            field=models.ManyToManyField(help_text='Sites onde o album ser\xe1 publicado', related_name='albums', verbose_name='sites', to='sites.Site'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='flickralbum',
            name='slug',
            field=models.SlugField(help_text='Utilizado para construir a url do album.', unique=True, max_length=130),
            preserve_default=True,
        ),
    ]
