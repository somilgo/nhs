# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_student_addedhours'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='is_senior',
            field=models.BooleanField(default=False, verbose_name=b'Check this box if you are a SENIOR (Grade 12)'),
        ),
        migrations.AlterField(
            model_name='student',
            name='is_second_year',
            field=models.BooleanField(verbose_name=b'Check this box if this is your SECOND YEAR in NHS'),
        ),
    ]
