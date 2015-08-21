# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20150821_0120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='current_students',
            field=models.ManyToManyField(to='events.Student', blank=True),
        ),
    ]
