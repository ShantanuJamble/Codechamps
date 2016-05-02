from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from .models import *
# Register your models here.


class AnswerInline(admin.TabularInline):
    model = Answer


class MCQForm(forms.ModelForm):
    """
    below is from
    http://stackoverflow.com/questions/11657682/
    django-admin-interface-using-horizontal-filter-with-
    inline-manytomany-field
    """

    class Meta:
        model = QuizModel
        exclude = []

    quiz = forms.ModelMultipleChoiceField(
        queryset=QuizModel.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name='Quizzes',
            is_stacked=False))


class MCQuestionAdmin(admin.ModelAdmin):
    list_display = ('content',)
    form = MCQForm
    search_fields = ('content', 'explanation')
    filter_horizontal = ('quiz',)
    inlines = [AnswerInline]



admin.site.register(MCQuestion, MCQuestionAdmin)
admin.site.register(Sitting, admin.ModelAdmin)
