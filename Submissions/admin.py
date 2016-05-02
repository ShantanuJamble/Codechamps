from django.contrib import admin

# Register your models here.
from .models import Submission
class Submissionadmin(admin.ModelAdmin):
    class Meta:
        model=Submission
admin.site.register(Submission,Submissionadmin)