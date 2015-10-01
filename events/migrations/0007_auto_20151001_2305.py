# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_student_required_hours'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='hours',
            field=models.DecimalField(default=0, max_digits=10, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='student',
            name='points',
            field=models.DecimalField(default=0, max_digits=10, decimal_places=1),
        ),
    ]
