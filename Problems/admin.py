from django.contrib import admin

# Register your models here.
from Problems.models import Problem


class Problemadmin(admin.ModelAdmin):
    class Meta:
        model=Problem
admin.site.register(Problem,Problemadmin)