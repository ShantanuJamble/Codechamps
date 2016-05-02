from django.contrib import admin
from .models import Person, EmailConfirmed
# Register your models here.

class DeveloperAdmin(admin.ModelAdmin):
    class Meta:
        model = Person


admin.site.register(Person, DeveloperAdmin)

admin.site.register(EmailConfirmed)
