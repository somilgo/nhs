# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20150821_0124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='is_second_year',
            field=models.BooleanField(verbose_name=b'Check this box if you are a SENIOR'),
        ),
    ]
