from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from challenges.models import Category, QuizModel


class Problem(models.Model):
    title = models.CharField(max_length=50, unique=True, blank=False, null=False)
    body = models.TextField(max_length=2000, null=False, blank=False)
    test_count = models.IntegerField(default=0, null=False, blank=False)
    input_sample = models.TextField(max_length=100, blank=False, null=False)
    output_sample = models.TextField(max_length=100, blank=False, null=False)
    domain = models.ForeignKey(Category, null=True, blank=True, verbose_name="Category")
    test_time = models.IntegerField(default=4, blank=False, null=False)
    difficulty = models.CharField(default='easy', blank=False, null=False, max_length=8)
    added_by = models.ForeignKey(User, blank=True, null=True)
    quiz = models.ForeignKey(QuizModel, blank=True, null=True)

    def __str__(self):
        return str(self.id) + " " + str(self.title)