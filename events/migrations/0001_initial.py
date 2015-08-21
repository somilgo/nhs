# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('location', models.CharField(max_length=200)),
                ('date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('total_hours', models.DecimalField(max_digits=4, decimal_places=2)),
                ('total_points', models.DecimalField(max_digits=3, decimal_places=1)),
                ('max_students', models.IntegerField()),
                ('num_students', models.IntegerField(default=0)),
                ('event_description', models.TextField(default=b'')),
                ('event_completed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('firstname', models.CharField(default=b'', max_length=30, verbose_name=b'First Name')),
                ('lastname', models.CharField(default=b'', max_length=30, verbose_name=b'Last Name')),
                ('email', models.EmailField(default=b'', unique=True, max_length=255, verbose_name=b'Email Address')),
                ('is_officer', models.BooleanField(default=False)),
                ('is_second_year', models.BooleanField(verbose_name=b'Check this box if this is your second year in NHS')),
                ('hours', models.DecimalField(default=0, max_digits=5, decimal_places=2)),
                ('points', models.DecimalField(default=0, max_digits=3, decimal_places=1)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='event',
            name='current_students',
            field=models.ManyToManyField(to='events.Student'),
        ),
    ]
