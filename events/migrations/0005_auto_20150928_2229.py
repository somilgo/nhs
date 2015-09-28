# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_auto_20150928_2224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='total_points',
            field=models.DecimalField(default=0, max_digits=3, decimal_places=1),
        ),
    ]
