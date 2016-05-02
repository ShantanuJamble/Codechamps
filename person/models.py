from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail, EmailMessage
from django.template import Context
from django.utils.encoding import smart_unicode
from django.template.loader import get_template

from Classrooms.settings import EMAIL_HOST_USER
# Create your models here.
from college.models import College


class Person(models.Model):

    user = models.OneToOneField(User)
    propic = models.ImageField(upload_to="profilepics/", null=True, blank=True)
    joined_on = models.DateField(auto_now_add=True, auto_now=False)
    solved_count = models.IntegerField(blank=False, default=0)
    role = models.CharField(max_length=10)
    college=models.ForeignKey(College,null=True)

    def __unicode__(self):
        return smart_unicode(self.user.first_name)


# model to verify users
class EmailConfirmed(models.Model):
    user = models.OneToOneField(User)
    activation_key = models.CharField(max_length=200, null=True, blank=True)
    confirmed = models.BooleanField(default=False)

    def __unicode__(self):
        return str(self.user.username) + str(self.confirmed)

    def active_user_email(self):
        activation_url = "http://localhost:8000/user/activate/%s" % self.activation_key
        # activation_url = "http://117.208.48.173:8000/user/activate/%s" % (self.activation_key)
        context = {
            "activation_url": activation_url,
            "user": self.user.username,
        }
        # message = render_to_string("activation_email.txt", context)
        subject = 'Activate Your Account'
        message = get_template('mail_templates/activation_mail.html').render(Context(context))
        # print message
        self.email_user(subject, message, EMAIL_HOST_USER)

    def email_user(self, subject, message, from_email=None, *kwargs):
        # send_mail(subject, message, from_email, [self.user.email, ], *kwargs)
        message = EmailMessage(subject, message, to=[self.user.email], from_email=from_email)
        message.content_subtype = 'html'
        message.send()


'''class UserProfile(models.Model):
    username = models.CharField(blank=False, null=False)
    language_preferred = models.TextField(max_length=200, null=True, default=None)
    frameworks = models.TextField(max_length=200, null=True, default=None)
    courses_taken = models.IntegerField(blank=True)
    contact_no = models.IntegerField(max_length=10,blank=true)'''
