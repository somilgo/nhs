# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_student_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='addedHours',
            field=models.DecimalField(default=0, max_digits=10, decimal_places=2),
        ),
    ]
