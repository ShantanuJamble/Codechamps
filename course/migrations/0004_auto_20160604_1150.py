# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0003_auto_20160604_1149'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, default=1, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='course',
            name='code',
            field=models.CharField(max_length=5),
            preserve_default=True,
        ),
    ]
