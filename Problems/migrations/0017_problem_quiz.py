# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0002_quizmodel_display_picture'),
        ('Problems', '0016_remove_problem_quiz'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='quiz',
            field=models.ManyToManyField(to='challenges.QuizModel', null=True, blank=True),
            preserve_default=True,
        ),
    ]
