from college.models import College

__author__ = 'shantya'
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Person

# Registration Form

class RegistraionForm(ModelForm):
    username = forms.CharField(label='User name')
    email = forms.EmailField(label='Email')
    name = forms.CharField(label='Name')
    password = forms.CharField(label='Password', widget=forms.PasswordInput(render_value=False))
    password1 = forms.CharField(label='Verify Password', widget=forms.PasswordInput(render_value=False))
    college=forms.CharField(label='College',max_length=200)
    role = forms.CharField()

    class Meta:
        model = Person
        exclude = ('user', 'propic', 'solved_count','role','college')

    # CHECKING VALID USERNAME
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError('Username not available select another')

    # #check valid email-id

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            user = User.objects.get(email=email)
            raise forms.ValidationError("Some account is already linked with this email id.")
        except User.DoesNotExist:
            return email

    # password matching
    def clean(self):
        if 'password' in self.cleaned_data and 'password1' in self.cleaned_data and self.cleaned_data['password'] != \
                self.cleaned_data['password1']:
            raise forms.ValidationError("The password does not match ")
        return self.cleaned_data


# login form
class LoginForm(forms.Form):
    username = forms.CharField(label='username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput(render_value=False))


# RESET FORM
class ResetForm(forms.Form):
    email = forms.EmailField(label="Youe Email-ID")


# update form
class UpdateForm(forms.Form):
    name = forms.CharField(label='name')
    country = forms.CharField(label='country')


#password reset form
class PasswordResetForm(forms.Form):
    password = forms.CharField(label='Password', widget=forms.PasswordInput(render_value=False))
    password1 = forms.CharField(label='Password1', widget=forms.PasswordInput(render_value=False))