from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from college.models import College
from person.models import Person


class Course(models.Model):
    title = models.CharField(max_length=10, blank=False, null=False)
    code = models.CharField(max_length=5, blank=False, null=False,unique=True)
    description = models.TextField(max_length=5000, blank=True, null=True)
    teacher = models.ForeignKey(Person, blank=False, null=False)
    students = models.ManyToManyField(User, blank=True, null=True)
    active = models.BooleanField(default=True, help_text='Course Status')
    college = models.ForeignKey(College)

    def __str__(self):
        return self.title
