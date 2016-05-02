# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0002_quizmodel_display_picture'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.CharField(help_text='Enter the answer text that you want displayed', max_length=1000, verbose_name='Content')),
                ('correct', models.BooleanField(default=False, help_text='Is this a correct answer?', verbose_name='Correct')),
            ],
            options={
                'verbose_name': 'Answer',
                'verbose_name_plural': 'Answers',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.CharField(help_text='Enter the question text that you want displayed', max_length=1000, verbose_name='Question')),
                ('explanation', models.TextField(help_text='Explanation to be shown after the question has been answered.', max_length=2000, verbose_name='Explanation', blank=True)),
            ],
            options={
                'ordering': ['category'],
                'verbose_name': 'Question',
                'verbose_name_plural': 'Questions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MCQuestion',
            fields=[
                ('question_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='mcqs.Question')),
                ('answer_order', models.CharField(choices=[('content', 'Content'), ('random', 'Random'), ('none', 'None')], max_length=30, blank=True, help_text='The order in which multichoice answer options are displayed to the user', null=True, verbose_name='Answer Order')),
            ],
            options={
                'verbose_name': 'Multiple Choice Question',
                'verbose_name_plural': 'Multiple Choice Questions',
            },
            bases=('mcqs.question',),
        ),
        migrations.CreateModel(
            name='Sitting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question_order', models.CommaSeparatedIntegerField(max_length=1024, null=True, verbose_name='Questions_Order', blank=True)),
                ('programs', models.CommaSeparatedIntegerField(max_length=1024, null=True, verbose_name='Questions_Order', blank=True)),
                ('complete', models.BooleanField(default=False, verbose_name='Complete')),
                ('answers_set', models.CommaSeparatedIntegerField(default=None, max_length=1024, verbose_name="User's Answers", blank=True)),
                ('score', models.PositiveIntegerField(default=0, verbose_name='Score')),
                ('start_time', models.DateTimeField(default=None, help_text='Participant Start Time', null=True)),
                ('end_time', models.DateTimeField(default=None, help_text='Participant End Time', null=True)),
                ('quiz', models.ForeignKey(verbose_name='Quiz', to='challenges.QuizModel')),
                ('user', models.ForeignKey(verbose_name='User', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='question',
            name='category',
            field=models.ForeignKey(to='challenges.Category', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='question',
            name='quiz',
            field=models.ManyToManyField(to='challenges.QuizModel', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(verbose_name='Question', to='mcqs.MCQuestion'),
            preserve_default=True,
        ),
    ]
