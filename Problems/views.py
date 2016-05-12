import os
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response, Http404, HttpResponseRedirect
from django.template import RequestContext
from Problems.forms import addProblemForm
from challenges.models import Category, QuizModel
from mcqs.models import Sitting
from .models import Problem
from person.models import Person
from Submissions.models import Submission

# Create your views here.
__author__ = 'shantya'

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# #View to handle the file uploads
def upload_files(request, path, type):
    files = type + '_files'
    for count, x in enumerate(request.FILES.getlist(files)):
        def handle_uploaded_file(f):
            with open(path + '\\' + type + "_" + str(count) + '.txt', 'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)

        handle_uploaded_file(x)


def get_files(request, title):
    title = title.replace(" ", '_')
    path = os.path.join(BASE_DIR, 'static', 'media', 'input', title)
    if os.path.exists(path) is False:
        os.makedirs(path)
    upload_files(request, path, 'input')
    path = os.path.join(BASE_DIR, 'static', 'media', 'output', title)
    if os.path.exists(path) is False:
        os.makedirs(path)
    upload_files(request, path, 'output')
    return


def get_category():
    try:
        category_list = Category.objects.all()
    except:
        category_list = None
    return category_list


def get_quiz(person):
    try:
        quiz_list = QuizModel.objects.all().filter(added_by=person)
    except:
        quiz_list = None
    return quiz_list


@login_required(login_url='/login')
def add_problems(request):
    # Add code to check wheter the request.user is TEACHER
    category_list = get_category()
    person = Person.objects.get(user=request.user)
    quiz_list = get_quiz(person)

    if request.method == 'POST':
        form = addProblemForm(request.POST, request.FILES)
        print form.is_valid()
        if form.is_valid():
            title = form.cleaned_data['title']
            body = form.cleaned_data['body']
            test_count = form.cleaned_data['test_count']
            input_sample = form.cleaned_data['input_sample']
            output_sample = form.cleaned_data['output_sample']
            domain = Category.objects.get(category=form.cleaned_data['domain'])
            difficulty = form.cleaned_data['difficulty']
            test_time = form.cleaned_data['test_time']
            try:
                quiz = QuizModel.objects.get(title=form.cleaned_data['quiz'])
            except:
                quiz = None
            problem = Problem(title=title, body=body, difficulty=difficulty, test_count=test_count,
                              input_sample=input_sample,
                              output_sample=output_sample, domain=domain, test_time=test_time, added_by=request.user,
                              quiz=quiz)
            problem.save()
            get_files(request, title)
            message = 'Problem added Succesfully!!'
            return render_to_response('add_problem.html',
                                      {'message': message, 'form': form, 'category_list': category_list,
                                       'person': person, 'quiz_list': quiz_list},
                                      context_instance=RequestContext(request))
        else:
            message = 'Sorry!Something went wrong'
            return render_to_response('add_problem.html',
                                      {'message': message, 'form': form, 'category_list': category_list,
                                       'person': person, 'quiz_list': quiz_list},
                                      context_instance=RequestContext(request))
    else:
        form = addProblemForm
        return render_to_response('add_problem.html',
                                  {'message': '', 'form': form, 'category_list': category_list, 'person': person,
                                   'quiz_list': quiz_list},
                                  context_instance=RequestContext(request))


# #####
# PROBLEM MODIFY VIEW
@login_required(login_url='/login')
def modify_problem(request, problem_id):
    # Add author authentication here
    category_list = get_category()
    person = Person.objects.get(user=request.user)
    quiz_list = get_quiz(person)
    try:
        problem = Problem.objects.get(id=problem_id)
    except Problem.DoesNotExist:
        problem = None
    if request.method == 'POST':
        if problem:
            form = addProblemForm(request.POST, request.FILES)
            if form.is_valid():
                print type(form.cleaned_data['quiz'])
                problem.title = form.cleaned_data['title']
                problem.body = form.cleaned_data['body']
                problem.test_count = form.cleaned_data['test_count']
                problem.input_sample = form.cleaned_data['input_sample']
                problem.output_sample = form.cleaned_data['output_sample']
                problem.domain = Category.objects.get(category=form.cleaned_data['domain'])
                problem.difficulty = form.cleaned_data['difficulty']
                problem.test_time = form.cleaned_data['test_time']
                problem.quiz = (QuizModel.objects.get(title=form.cleaned_data['quiz']))
                problem.save()
                get_files(request, problem.title)
                message = 'Problem Updated Succesfully!!'
                return render_to_response('modify_problem.html', {'message': message, 'form': form, 'problem': problem,
                                                                  'category_list': category_list, 'person': person,
                                                                  'quiz_list': quiz_list},
                                          context_instance=RequestContext(request))
            else:
                message = 'Sorry!Something went wrong'
                return render_to_response('modify_problem.html',
                                          {'message': message, 'form': form, 'category_list': category_list,
                                           'person': person, 'quiz_list': quiz_list},
                                          context_instance=RequestContext(request))
        else:
            message = 'Problem Does Not exists'
            return render_to_response('modify_problem.html',
                                      {'message': message, 'form': addProblemForm, 'problem': problem,
                                       'category_list': category_list, 'person': person, 'quiz_list': quiz_list},
                                      context_instance=RequestContext(request))
    else:
        if problem:
            message = 'Problem found'
        else:
            message = 'Problem not found'
        return render_to_response('modify_problem.html',
                                  {'message': message, 'form': addProblemForm, 'problem': problem,
                                   'category_list': category_list, 'person': person, 'quiz_list': quiz_list},
                                  context_instance=RequestContext(request))


# ##Display practise page This is for student.
def all_problems(request):
    status = False
    person = None
    solved_list = []
    if request.user.is_authenticated():
        status = True
        person = Person.objects.get(user=request.user)
        submissions = Submission.objects.filter(person=request.user.username).filter(status='AC')
        for solution in submissions:
            solved_list.append(solution.problem_id)
    problems = Problem.objects.all().filter(domain=Category.objects.get(category='Practise'))
    return render_to_response("practise.html", {'message': status, 'problems': problems, 'person': person,
                                                'solved_list': solved_list},
                              context_instance=RequestContext(request))


# #Single problem Page
@login_required(login_url='/login')
def problem_page(request, problem_id):
    message = False
    person = None
    total_submissions = 0
    person_submission = 0
    person_submission_count = 0
    accepted_submission = 0
    if request.user.is_authenticated():
        message = True
        person = Person.objects.get(user=request.user)
    try:
        problem = Problem.objects.get(id=problem_id)
        problem.input_sample = "<br>".join(problem.input_sample.split("\n"))
        problem.output_sample = "<br>".join(problem.output_sample.split("\n"))
        max_marks = problem.test_count * 10
        total_submissions = Submission.objects.filter(problem_id=problem_id)
        person_submission = total_submissions.filter(person=request.user.username)
        person_submission_count = person_submission.count()
        accepted_submission = total_submissions.filter(status='AC').count()
        total_submissions = total_submissions.count()
    except Problem.DoesNotExist:
        problem = None
    # context = {'message': message, 'problem': problem, 'person': person}
    if request.is_ajax() is True:
        return render_to_response("raw_poblem_page.html", locals(), context_instance=RequestContext(request))
    else:
        return render_to_response("problem_page.html", locals(), context_instance=RequestContext(request))


# this is for teacher
@login_required(login_url='/login')
def list_problems(request):
    prob_list = None
    person = Person.objects.get(user=request.user)
    try:
        prob_list = Problem.objects.all().filter(added_by=request.user)
    except:
        prob_list = None
    return render_to_response("problem_list_page.html", locals(), context_instance=RequestContext(request))


# this is for quiz ajax request
def get_program(request, slug):
    problem = None
    sitting_id = request.POST.get('sitting_id')
    try:
        problem = Problem.objects.get(id=int(slug))
        problem.input_sample = "<br>".join(problem.input_sample.split("\n"))
        problem.output_sample = "<br>".join(problem.output_sample.split("\n"))
        max_marks = problem.test_count * 10
    except:
        print 'question not found'
    try:
        sitting_id = request.POST.get('sitting_id')

    except:
        print 'sitting id not in request'
    marks = 0
    try:
        sitting = Sitting.objects.get(id=sitting_id)
        marks = sitting.score
    except:
        marks = 0
    return render_to_response('raw_poblem_page.html', locals(), context_instance=RequestContext(request))


# this method add question to a quiz
def add_prgs(prgs, quiz):
    for m in prgs:
        q = Problem.objects.get(id=int(m))
        q.quiz = quiz
        try:
            q.save()
        except:
            print 'save failed'


def delete_prgs(prgs, quiz, all=False):
    all_prgs = Problem.objects.all()
    if not all:
        for q in all_prgs:
            print str(q.id) not in prgs and quiz == q.quiz
            if str(q.id) not in prgs and quiz == q.quiz:
                q.quiz = None
            try:
                q.save()
            except:
                print 'save failed'
    else:
        for q in all_prgs:
            q.quiz = None
            try:
                q.save()
            except:
                print 'save failed'


def prg_to_quiz(request):
    print request.user.is_authenticated()
    if not request.user.is_authenticated():
        message = '404'
        return render_to_response('404.html', locals(), context_instance=RequestContext(request))
    person = Person.objects.get(user=request.user)
    if person.role != "TEACHER":
        message = '404'
        return render_to_response('404.html', locals(), context_instance=RequestContext(request))
    else:
        quiz = QuizModel.objects.get(id=request.GET['quiz'])
        prgs = []
        try:
            data = str(request.POST.getlist(u'prgs'))
            print data
            for d in data:
                try:
                    i = int(d)
                    prgs.append(d)
                except:
                    pass
            print(prgs)
        except:
            prgs = None
        print prgs
        if prgs:
            if str(request.GET['to_do']) == 'add':
                add_prgs(prgs, quiz)
            elif str(request.GET['to_do']) == 'delete':
                delete_prgs(prgs, quiz)
        else:
            delete_prgs(prgs, quiz, True)
        return HttpResponseRedirect('/quiz_dashboard/' + str(quiz.id))