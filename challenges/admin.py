from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from Problems.models import Problem

from .models import QuizModel, Category, SubCategory
# Register your models here.
'''
class QuizAdminForm(forms.ModelForm):
    """
    below is from
    http://stackoverflow.com/questions/11657682/
    django-admin-interface-using-horizontal-filter-with-
    inline-manytomany-field
    """

    class Meta:
        model = QuizModel
        exclude = []
    problem = forms.ModelMultipleChoiceField(
        queryset=Problem.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name='Problems',
            is_stacked=False))'''
class QuizAdmin(admin.ModelAdmin):
    #form = QuizAdminForm
    list_display = ('title', 'category',)
    list_filter = ('category',)
    search_fields = ('description', 'category', )


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('category', )


class SubCategoryAdmin(admin.ModelAdmin):
    search_fields = ('sub_category', )
    list_display = ('sub_category', 'category',)
    list_filter = ('category',)


admin.site.register(QuizModel, QuizAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)