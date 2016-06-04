from __future__ import unicode_literals
import re
import json

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, ImproperlyConfigured
from django.core.validators import MaxValueValidator
from django.db import models
from django.utils.translation import ugettext as _
from django.utils.timezone import now
from django.utils.encoding import python_2_unicode_compatible


# Create your models here
from person.models import Person


class CategoryManager(models.Manager):
    def new_category(self, category):
        new_category = self.create(category=re.sub('\s+', '-', category)
                                   .lower())

        new_category.save()
        return new_category


@python_2_unicode_compatible
class Category(models.Model):
    category = models.CharField(
        verbose_name=_("Category"),
        max_length=250, blank=True,
        unique=True, null=True)

    objects = CategoryManager()

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.category


@python_2_unicode_compatible
class SubCategory(models.Model):
    sub_category = models.CharField(
        verbose_name=_("Sub-Category"),
        max_length=250, blank=True, null=True)

    category = models.ForeignKey(
        Category, null=True, blank=True,
        verbose_name=_("Category"))

    objects = CategoryManager()

    class Meta:
        verbose_name = _("Sub-Category")
        verbose_name_plural = _("Sub-Categories")

    def __str__(self):
        return self.sub_category + " (" + self.category.category + ")"


@python_2_unicode_compatible
class QuizModel(models.Model):
    title = models.CharField(verbose_name=_("Title"), max_length=20, blank=False,unique=True)

    description = models.TextField(verbose_name=_("Description"), blank=True, help_text=_("a description of the quiz"))

    url = models.SlugField(max_length=60, blank=False, help_text=_("a user friendly url"),
                           verbose_name=_("user friendly url"))

    category = models.ForeignKey(Category, null=True, blank=True, verbose_name=_("Category"))

    random_order = models.BooleanField(blank=False, default=False, verbose_name=_("Random Order"),
                                       help_text=_("Display the questions in "
                                                   "a random order or as they "
                                                   "are set?"))
    single_attempt = models.BooleanField(blank=False, default=False, verbose_name=_("Single Attempt"),
                                         help_text=_("Only one chance to "
                                                     "attempt the quiz"))
    start_time = models.DateTimeField(help_text="Event start Time", blank=False, null=True, default=None)
    end_time = models.DateTimeField(help_text="Event End Time", blank=False, null=True, default=None)
    duration = models.IntegerField(help_text="Event Duration in minuets", blank=False, null=True, default=None)
    participants = models.ManyToManyField(User, blank=True, null=True)
    display_picture = models.ImageField(upload_to='competitions/',blank=True,null=True)
    added_by=models.ForeignKey(Person,null=False,blank=False,default=1)
    unique_together = ("t   itle", "url")

    class Meta:
        verbose_name = _("Quiz")
        verbose_name_plural = _("Quizzes")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return '/challenges/' + str(self.url) + '/'

    def is_question_order_random(self):
        return self.random_order
