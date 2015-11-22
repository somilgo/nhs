# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_auto_20151001_2305'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='phone',
            field=models.CharField(default=b'000-000-0000', max_length=12, verbose_name=b'Phone Number', validators=[django.core.validators.RegexValidator(regex=b'^[1-9]\\d{2}-\\d{3}-\\d{4}$', message=b"Phone number must be entered in the format: 'XXX-XXX-XXXX'")]),
        ),
    ]
