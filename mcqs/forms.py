from django import forms
from django.contrib.admin.utils import help_text_for_field
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms.widgets import RadioSelect, SelectMultiple
from .models import MCQuestion


class AddMcq2Quiz(forms.Form):
    choices = [(que.id, que.content) for que in MCQuestion.objects.all()]

    mcqs = forms.ModelMultipleChoiceField(
        queryset=MCQuestion.objects.all(),
        required=True,
        widget=FilteredSelectMultiple(attrs={'class': "form-control"},
                                      verbose_name='MCQs',
                                      is_stacked=False))
