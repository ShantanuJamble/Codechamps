from django.contrib import admin

# Register your models here.
from college.models import College

admin.site.register(College,admin.ModelAdmin)