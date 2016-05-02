from datetime import datetime

__author__ = 'shantya'
from django import forms
from django.forms import CheckboxInput, TextInput
from .models import Category
from datetimewidget.widgets import DateTimeWidget, DateWidget, TimeWidget

choices = [(cat.id, cat.category) for cat in Category.objects.all()]
duration = [(60, '1 hr'), (120, '2 hrs'), (180, '3 hrs'), (360, '6 hrs'), (720, '12 hrs'), (1440, '1 day'),
            (2880, '2 days'), (-1, 'Till the End of Quiz')]


class AddQuizForm(forms.Form):
    start_date_time = forms.DateTimeField(
        widget=DateTimeWidget(attrs={'class': "form-control", 'width': "50%"}, usel10n=True, bootstrap_version=3))
    end_date_time = forms.DateTimeField(
        widget=DateTimeWidget(attrs={'class': "form-control"}, usel10n=True, bootstrap_version=3))
    random = forms.BooleanField(widget=CheckboxInput, label='Random Order')
    single = forms.BooleanField(widget=CheckboxInput, label='Single Attempt')
    category = forms.ChoiceField(choices=choices, widget=forms.Select(attrs={'class': "form-control"}, ))
    duration = forms.ChoiceField(choices=duration, widget=forms.Select(attrs={'class': "form-control"}, ))
    title = forms.CharField(max_length=20,
                            widget=TextInput(attrs={'class': "form-control", 'placeholder': "Quiz Title"}),
                            required=True)


    def clean(self):
        start = self.cleaned_data['start_date_time']
        end = self.cleaned_data['end_date_time']
        # end=datetime.strptime(self.cleaned_data['end_date_time'], '%Y-%m-%d %H:%M:%S')
        if end <= start:
            raise forms.ValidationError("End Date Cannot be small than Start.")
        return self.cleaned_data

