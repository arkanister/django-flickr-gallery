# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_flickr_gallery', '0006_auto_20160222_1543'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photoset',
            fields=[
                ('photoset_id', models.CharField(max_length=20, serialize=False, verbose_name='photoset id', primary_key=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='creation date')),
            ],
            options={
                'ordering': ['-creation_date'],
                'verbose_name': 'photoset',
                'verbose_name_plural': 'photosets',
            },
            bases=(models.Model,),
        ),
    ]
