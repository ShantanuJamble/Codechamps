from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response

# Create your views here.
from django.template import RequestContext
from django.views.generic import ListView
from course.models import Course
from person.models import Person

@login_required(login_url='/')
def course_list(request):
    course_list = Course.objects.all()
    person = Person.objects.get(user=request.user)
    course_list=course_list.filter(college=person.college)
    return render_to_response('course_list.html', locals(), context_instance=RequestContext(request))
@login_required(login_url='/')
def add_course(request):
    person = Person.objects.get(user=request.user)
    if person.role == 'TEACHER':
        if request.method == 'POST':
            try:
                title = request.POST['title']
                description = request.POST['body']
                code = request.POST['code']
                print title, description, code
                new_course = Course(title=title, description=description, code=code,
                                    teacher=person, college=person.college)
                new_course.save()
            except Exception as e:
                print e
    else:
        return render_to_response('404.html', locals(), context_instance=RequestContext(request))
    return render_to_response('add_course.html', locals(), context_instance=RequestContext(request))


@login_required(login_url='/')
def course_dashboard(request, course_code):
    person = Person.objects.get(user=request.user)
    try:
        course = Course.objects.get(code=course_code)
        enrolled = False
        if person.role == 'STUDENT':
            if person.user in course.students.all():
                enrolled = True
        return render_to_response('course_dashboard.html', locals(), context_instance=RequestContext(request))
    except:
        return render_to_response('404.html', locals(), context_instance=RequestContext(request))


@login_required(login_url='/')
def enroll(request):
    person = Person.objects.get(user=request.user)
    task = request.GET['task']
    course_code = request.GET['course_code']
    print course_code
    try:
        course = Course.objects.get(code=course_code)
        course.students.add(request.user)
        if task == u'enroll':
            course.save()
            enrolled = True
            return course_dashboard(request, course_code)
        elif task == u'stats':
            # stas page
            count=course.students.count
            return render_to_response('course_stats.html', locals(), context_instance=RequestContext(request))
    except Exception as e:
        print e
        return render_to_response('404.html', locals(), context_instance=RequestContext(request))