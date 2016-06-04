# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('college', '0001_initial'),
        ('course', '0004_auto_20160604_1150'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='college',
            field=models.ForeignKey(default=2, to='college.College'),
            preserve_default=False,
        ),
    ]
