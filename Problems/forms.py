from django.core.exceptions import ValidationError

__author__ = 'shantya'

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Problem
# ##############################################################################
# ###MULTIPLE FILES HANDLE KARYLA navin widget define kela
# reference http://koensblog.eu/blog/7/multiple-file-upload-django/
class MultiFileInput(forms.FileInput):
    def render(self, name, value, attrs={}):
        attrs['multiple'] = 'multiple'
        return super(MultiFileInput, self).render(name, None, attrs=attrs)

    def value_from_datadict(self, data, files, name):
        if hasattr(files, 'getlist'):
            return files.getlist(name)
        else:
            return [files.get(name)]


class MultiFileField(forms.FileField):
    widget = MultiFileInput
    default_error_messages = {
        'min_num': u"Ensure at least %(min_num)s files are uploaded (received %(num_files)s).",
        'max_num': u"Ensure at most %(max_num)s files are uploaded (received %(num_files)s).",
        'file_size': u"File: %(uploaded_file_name)s, exceeded maximum upload size."
    }

    def __init__(self, *args, **kwargs):
        self.min_num = kwargs.pop('min_num', 0)
        self.max_num = kwargs.pop('max_num', None)
        self.maximum_file_size = kwargs.pop('maximum_file_size', None)
        super(MultiFileField, self).__init__(*args, **kwargs)

    def to_python(self, data):
        ret = []
        for item in data:
            ret.append(super(MultiFileField, self).to_python(item))
        return ret

    def validate(self, data):
        super(MultiFileField, self).validate(data)
        num_files = len(data)
        if len(data) and not data[0]:
            num_files = 0
        if num_files < self.min_num:
            raise ValidationError(self.error_messages['min_num'] % {'min_num': self.min_num, 'num_files': num_files})
            return
        elif self.max_num and num_files > self.max_num:
            raise ValidationError(self.error_messages['max_num'] % {'max_num': self.max_num, 'num_files': num_files})


###############################################################################
class addProblemForm(forms.Form):
    title = forms.CharField(label='title', max_length=50)
    body = forms.CharField(label='body', widget=forms.Textarea())
    input_sample = forms.CharField(label='input_sample', widget=forms.Textarea())
    output_sample = forms.CharField(label='output_sample', widget=forms.Textarea())
    test_count = forms.IntegerField(label='No. of test case files')
    test_time = forms.IntegerField(label='Time for each test case files')
    input_files = MultiFileField(max_num=10, min_num=1,)
    output_files = MultiFileField(max_num=10, min_num=1,)
    domain = forms.CharField(label='doamin', max_length=50)
    difficulty=forms.CharField(label='difficulty', max_length=8)
