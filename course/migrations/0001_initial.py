# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0002_person_college'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=10)),
                ('code', models.CharField(max_length=5)),
                ('active', models.BooleanField(default=True, help_text=b'Course Status')),
                ('students', models.ManyToManyField(to=settings.AUTH_USER_MODEL, null=True, blank=True)),
                ('teacher', models.ForeignKey(to='person.Person')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
