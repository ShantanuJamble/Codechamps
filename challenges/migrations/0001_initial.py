# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.CharField(max_length=250, unique=True, null=True, verbose_name='Category', blank=True)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QuizModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=60, verbose_name='Title')),
                ('description', models.TextField(help_text='a description of the quiz', verbose_name='Description', blank=True)),
                ('url', models.SlugField(help_text='a user friendly url', max_length=60, verbose_name='user friendly url')),
                ('random_order', models.BooleanField(default=False, help_text='Display the questions in a random order or as they are set?', verbose_name='Random Order')),
                ('single_attempt', models.BooleanField(default=False, help_text='Only one chance to attempt the quiz', verbose_name='Single Attempt')),
                ('start_time', models.DateTimeField(default=None, help_text='Event start Time', null=True)),
                ('end_time', models.DateTimeField(default=None, help_text='Event End Time', null=True)),
                ('duration', models.IntegerField(default=None, help_text='Event Duration in minuets', null=True)),
                ('category', models.ForeignKey(verbose_name='Category', blank=True, to='challenges.Category', null=True)),
                ('participants', models.ManyToManyField(to=settings.AUTH_USER_MODEL, null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Quiz',
                'verbose_name_plural': 'Quizzes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sub_category', models.CharField(max_length=250, null=True, verbose_name='Sub-Category', blank=True)),
                ('category', models.ForeignKey(verbose_name='Category', blank=True, to='challenges.Category', null=True)),
            ],
            options={
                'verbose_name': 'Sub-Category',
                'verbose_name_plural': 'Sub-Categories',
            },
            bases=(models.Model,),
        ),
    ]
