import random
import hashlib
import uuid
import re
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group, Permission
from django.core.mail import send_mail
from django.shortcuts import render_to_response, Http404, HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from Classrooms.settings import *
from college.models import College
from .models import Person, EmailConfirmed
from .forms import RegistraionForm, LoginForm, ResetForm, UpdateForm, PasswordResetForm
# Create your views here.
__author__ = 'shantya'

# HOME VIEW
def home(request):
    if request.user.is_authenticated():
        return redirect_to_profile(request)
    return render_to_response('index.html', {}, context_instance=RequestContext(request))


# REDIRECTS TO THE PROFILE PAGE
def redirect_to_profile(request):
    usernm = request.user.username
    red_link = '/profile/' + usernm
    return HttpResponseRedirect(red_link)


# REGISTRAION HANDLING

def register(request):
    if request.user.is_authenticated():
        return redirect_to_profile(request)
    if request.method == 'POST':
        form = RegistraionForm(request.POST)
        print form.is_valid()
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'],
                                            email=form.cleaned_data['email'],
                                            first_name=form.cleaned_data['name'],
                                            password=form.cleaned_data['password'],
            )
            user.save()
            person = Person(user=user, role=form.cleaned_data['role'])
            print form.cleaned_data['college']
            person.college, created = College.objects.get_or_create(name=form.cleaned_data['college'])
            # person.college =College.objects.get(name=form.cleaned_data['college'])
            person.save()
            if person.role == 'TEACHER':
                grp = Group.objects.get(name='teachers')
                user.is_staff = True
                user.groups.add(grp)
                user.save()
            activation_key = get_activation_key(user)
            email_confirmed = EmailConfirmed(user=user, activation_key=activation_key, confirmed=False)
            email_confirmed.save()
            email_confirmed.active_user_email()
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])

            login(request, user)
            return HttpResponseRedirect('/login/')
        else:
            return render_to_response('register.html', {'form': form}, context_instance=RequestContext(request))
    else:
        # show blank form
        form = RegistraionForm
        context = {'form': form}
        return render_to_response('register.html', context, context_instance=RequestContext(request))


# Activation Key Creation
def get_activation_key(user):
    short_hash = hashlib.sha1(str(random.random())).hexdigest()[:5]
    username, domain = user.email.split('@')
    activation_key = hashlib.sha1(short_hash + username).hexdigest()
    return activation_key


# sends the activation mail to cerify the email on registration
SHA1_re = re.compile('^[a-f0-9]{40}$')


def activation_view(request, activation_key):
    if SHA1_re.search(activation_key):
        try:
            user_confirmed = EmailConfirmed.objects.get(activation_key=activation_key)
        except EmailConfirmed.DoesNotExist:
            user_confirmed = None
            raise Http404
        if user_confirmed is not None and not user_confirmed.confirmed:
            user_confirmed.confirmed = True
            user_confirmed.activation_key = 'Confirmed'
            user_confirmed.save()

        message = 'Your account is now activated!!'
    else:
        message = "It's Not a valid URL"
    return render_to_response('activation_page.html', locals())


# LOGIN REQUEST

def loginRequest(request):
    if request.user.is_authenticated():
        return redirect_to_profile(request)
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                try:
                    user = User.objects.get(email=username)
                except User.DoesNotExist:
                    user = None
            if user is not None:
                username = user.username
                dev_user = authenticate(username=username, password=password)
                if dev_user is not None:
                    login(request, dev_user)
                    red_link = '/profile/' + username
                    return HttpResponseRedirect(red_link)
                else:
                    return render_to_response('login.html', {'form': form, 'message': "Invalid credentials"},
                                              context_instance=RequestContext(request))
            else:
                return render_to_response('login.html', {'form': form, 'message': "Invalid credentials"},
                                          context_instance=RequestContext(request))
        else:
            return render_to_response('login.html', {'form': form},
                                      context_instance=RequestContext(request))
    else:
        form = LoginForm
        return render_to_response('login.html', {'form': form},
                                  context_instance=RequestContext(request))


# PROFILE DISPLAY
def profile(request, username):
    user = User.objects.get(username=username)
    person = Person.objects.get(user=user)
    if user == request.user:
        person_profile = person
        message = 'null'
        user_confirmed = EmailConfirmed.objects.get(user=user)
        if not user_confirmed.confirmed:
            activate_message = 'Please verify your email address!Check out you inbox'
    else:
        person_profile = person
        person = Person.objects.get(user=request.user)
        message = 'Follow'
    # context = {'person': person, 'message': message, 'person_profile': person_profile}
    return render_to_response('profile.html', locals(), context_instance=RequestContext(request))


# ##LOGOUT REQUEST

def logoutRequest(request):
    logout(request)
    return HttpResponseRedirect('/')


# #UPDATE PROFILE PIC
def upload_profile_pic(request):
    dev = Person.objects.get(user=request.user)
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    if request.method == 'POST':
        dev = Person.objects.get(user=request.user)
        dev.propic.delete(True)
        dev.propic = request.FILES['image']
        dev.save()
        red_link = '/profile/' + request.user.username
        return HttpResponseRedirect(red_link)


# remove profile pic
def remove_profile_pic(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        dev = Person.objects.get(user=request.user)
        dev.propic.delete(True)
        red_link = '/profile/' + request.user.username
        return HttpResponseRedirect(red_link)


# #FORGET PASSWORD
def reset_password(request):
    form = ResetForm(request.POST)
    status = 'False'
    if request.method == "POST":

        if form.is_valid():
            email = form.cleaned_data['email']
            message, status = sendMail(request, email)
            context = {'message': message, 'status': status}
            return render_to_response('mail_success.html', context, context_instance=RequestContext(request))
        else:
            Error = "email-id does not exists"
            return render_to_response('mail_success.html', {'form': form, 'error': Error, 'status': status},
                                      context_instance=RequestContext(request))
    else:
        Error = "Something went wrong please re-eneter the email id"
        return render_to_response('reset_password.html', {'form': form, 'error': Error, 'status': status},
                                  context_instance=RequestContext(request))


# ##MAIL SENDING FUNCTION
def sendMail(request, email):
    try:
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return 'This Email id does not exits!! ', 'False'
        password = str(uuid.uuid4())[:11].replace('-', '').lower()
        user.set_password(password)
        user.save()
        subject = 'Password reset'
        body = 'You requested a password reset .\n Below is the new login username password for you account,make sure you change it later \n Username=' + user.username + '\nPassword=' + password;
        list_emails = [email, ]
        from_email = EMAIL_HOST_USER
        send_mail(subject, body, from_email, list_emails, fail_silently=False)
        return 'Check your inbox.Thank you!!', 'True'
    except:
        return 'mail not sent', 'False'


# #USER PROFILE SETTINGS UPDATE
def settings(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    dev = Person.objects.get(user=request.user)
    return render_to_response('settings.html', {'person': dev}, context_instance=RequestContext(request))


# #Update Profile
def update_profile(request):
    if request.method == 'POST':
        form = UpdateForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            country = form.cleaned_data['country']
            user = request.user
            user.first_name = name
            user.save()
            dev = Person.objects.get(user=user)
            dev.country = country
            dev.save()
            return render_to_response('updatesuccess.html', {'message': 'success'},
                                      context_instance=RequestContext(request))
        else:
            return render_to_response('updatesuccess.html', {'message': 'error'},
                                      context_instance=RequestContext(request))
    else:
        return render_to_response('updatesuccess.html', {'message': 'error'}, context_instance=RequestContext(request))


# #PAssword Update
def password_change(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user = request.user
            user.set_password(password)
            user.save()
            return render_to_response('updatesuccess.html', {'message': 'success'},
                                      context_instance=RequestContext(request))
        else:
            return render_to_response('updatesuccess.html', {'message': 'error'},
                                      context_instance=RequestContext(request))
    else:
        return render_to_response('updatesuccess.html', {'message': 'error'}, context_instance=RequestContext(request))


def search_bar(request):
    query = request.GET['search-term']
    print query
    results = Person.objects.all().filter(name__contains=query)[5]
    return render_to_response('searchbar_template.html', locals(), context_instance=RequestContext(request))