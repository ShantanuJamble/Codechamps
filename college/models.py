from django.db import models

# Create your models here.

class College(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False, default='ABC')

    def __str__(self):
        return self.name
