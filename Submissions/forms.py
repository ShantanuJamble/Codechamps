__author__ = 'user'

from django import forms
from django_ace import AceWidget

class SubmissionForm(forms.Form):
    problem_id = forms.IntegerField(label='Problem_id')
    source = forms.CharField(widget=AceWidget)
    lang_chosen = forms.CharField(label="language", max_length="10")
