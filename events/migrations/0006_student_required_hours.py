# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_auto_20150928_2229'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='required_hours',
            field=models.DecimalField(default=12, max_digits=3, decimal_places=1),
        ),
    ]
