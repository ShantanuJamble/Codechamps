from django.db import models

# Create your models here.


class Submission(models.Model):
    problem_id = models.IntegerField(blank=False, null=False, )
    person = models.CharField(max_length=30, blank=False, null=False)
    status = models.CharField(max_length=10, blank=False, null=False)
    memory_used = models.FloatField(blank=False, null=False)
    date_time = models.DateTimeField(blank=False, null=False, auto_now_add=True, auto_now=False)
    lang_chosen=models.CharField(max_length=10,null=False,blank=False,default='cpp')
    marks = models.IntegerField(blank=False, null=False, default=0)

    def __str__(self):
        return str(self.problem_id) + " " + self.person + " " + str(self.date_time)