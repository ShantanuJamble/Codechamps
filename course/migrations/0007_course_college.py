# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('college', '0001_initial'),
        ('course', '0006_remove_course_college'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='college',
            field=models.ForeignKey(default=0, to='college.College'),
            preserve_default=False,
        ),
    ]
