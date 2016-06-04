from datetime import datetime, timedelta
import time
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import timezone
from django.views.generic.list import ListView
from Problems.models import Problem
from Submissions.models import Submission
from challenges.forms import AddQuizForm
from mcqs.forms import AddMcq2Quiz
from person.models import Person
from .models import QuizModel, Category
from mcqs.models import Sitting, MCQuestion


class QuizListView(ListView):
    model = QuizModel
    context_object_name = 'quiz_list'

    def get_context_data(self, **kwargs):
        context = super(QuizListView, self).get_context_data(**kwargs)
        quiz_list = QuizModel.objects.all()
        context['quiz_list'] = quiz_list
        context['person'] = Person.objects.get(user=self.request.user)
        return context


@login_required(login_url='/login')
def start_quiz(request, quiz_id):
    new_sitting = None
    quiz = QuizModel.objects.get(id=quiz_id)
    person = Person.objects.get(user=request.user)
    new_sitting = Sitting.objects.user_sitting(request.user, quiz)
    if not new_sitting:
        allowed = False
        message = 'You have completed the test already!'
    else:
        allowed = True
        questions = None
        programs = None
        if new_sitting.question_order is not None:
            questions = str(new_sitting.question_order)
            questions = questions.split(',')

        if new_sitting.programs is not None:
            programs = str(new_sitting.programs)
            programs = programs.split(',')
        try:
            if new_sitting.start_time is None:
                new_sitting.start_time = datetime.now()
                new_sitting.end_time = datetime.now() + timedelta(minutes=int(quiz.duration))
                milliseconds = time.mktime(new_sitting.end_time.timetuple()) * 1000
                new_sitting.save()
            else:
                milliseconds = new_sitting.end_time - timezone.now()
                milliseconds = datetime.now() + milliseconds
                milliseconds = time.mktime(milliseconds.timetuple())
                if milliseconds <= 0:
                    milliseconds = 0
                else:
                    milliseconds *= 1000

        except:
            print "Session Object creation failed"
            allowed = False
        question_set = []
        index = 0
        question_count = len(questions)
        while index < question_count:
            question_set.append(int(questions[index]))
            index += 1
    return render_to_response('mcqs/quiz_form.html', locals(), context_instance=RequestContext(request))


def exit_quiz(request, quiz_id):
    new_sitting = None
    quiz = QuizModel.objects.get(id=quiz_id)
    person = Person.objects.get(user=request.user)
    new_sitting = Sitting.objects.user_sitting(request.user, quiz)
    try:
        new_sitting.complete = True
        programs = new_sitting.programs.split(',')
        print programs
        prg_marks = 0
        for prg in programs:
            tmp_marks = 0
            submissions = Submission.objects.all().filter(problem_id=int(prg))
            for sub in submissions:
                print sub
                if tmp_marks < int(sub.marks):
                    tmp_marks = int(sub.marks)
                print tmp_marks
            prg_marks += tmp_marks
        try:
            new_sitting.score = prg_marks + int(new_sitting.score)
        except Exception as e:
            print e
        print new_sitting.score
        new_sitting.save()
    except:
        print 'Saving failed'
    return render_to_response('challenges/results.html', locals(), context_instance=RequestContext(request))


def quiz_take(request, quiz):
    if request.user.is_authenticated():
        quiz = QuizModel.objects.get(url=quiz)
        new_sitting = Sitting.objects.user_sitting(request.user, quiz)
        person = Person.objects.get(user=request.user)
        try:
            user = quiz.participants.get(username=request.user.username)
        except Exception:
            user = None
        now = timezone.now()
        start = quiz.start_time
        end = quiz.end_time
        count = quiz.participants.count()
        if user is None and start <= now < end and new_sitting.complete is False:
            message = "Register"
        else:
            if new_sitting is False:
                message = "Completed"
            elif now > start and new_sitting.complete is False:
                message = "Started"
            elif new_sitting.complete is True:
                if now >= end:
                    message = "Ended"
                else:
                    message = "Completed"
            elif now < start and new_sitting.complete is False:
                message = "Participated"
                # start_quiz(quiz, request)
    else:
        allowed = False
        message = 'Dude you aren\'t logged in'

    return render_to_response('mcqs/quiz_form.html', locals(), context_instance=RequestContext(request))


# Register method for quiz
def register(request, quiz_id):
    if request.user.is_authenticated():
        try:
            quiz = QuizModel.objects.get(id=quiz_id)
            quiz.participants.add(request.user)
            quiz.save()
            return HttpResponseRedirect(quiz.get_absolute_url())
        except QuizModel.DoesNotExist:
            print 'Quiz Object not found'
    else:
        pass


# create a new quiz
@login_required(login_url='/login')
def add_quiz(request):
    form = AddQuizForm()
    person = Person.objects.get(user=request.user)
    message = ''
    if person.role == 'TEACHER':
        if request.method == 'POST':
            form = AddQuizForm(request.POST)
            print form.is_valid()
            print request.FILES['dp']
            # request_dict = datetime.strptime(request_dict, '%Y-%m-%d %H:%M:%S')
            if form.is_valid():
                title = request.POST.get('title')
                url = title.lower().replace(' ', '_')
                desc = request.POST.get('body')
                single = False
                category = Category.objects.get(id=int(request.POST.get('category')))
                if request.POST.get('single') == 'on':
                    single = True
                random = False
                if request.POST.get('random') == 'on':
                    random = True
                start_date_time = form.cleaned_data['start_date_time']
                end_date_time = form.cleaned_data['end_date_time']
                duration = int(request.POST.get('duration'))
                if duration == -1:
                    duration = end_date_time - start_date_time
                    duration = int((duration.total_seconds()) / 60)
                quiz = QuizModel(title=title, description=desc, url=url, single_attempt=single, random_order=random,
                                 category=category, start_time=start_date_time, end_time=end_date_time, added_by=person,
                                 duration=duration)
                quiz.display_picture = request.FILES['dp']
                quiz.save()
                message = 'Quiz Added Successfully'
                return HttpResponseRedirect('/quiz_dashboard/' + str(quiz.id))
            else:
                message = 'Sorry Something Went wrong. Please try again!'
                return render_to_response('add_new_quiz.html', locals(), context_instance=RequestContext(request))
        return render_to_response('add_new_quiz.html', locals(), context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')


@login_required(login_url='/')
def quiz_dashboard(request, slug):
    try:
        person = Person.objects.get(user=request.user)
    except:
        person = None
    if person.role == 'TEACHER':
        try:
            quiz = QuizModel.objects.get(id=int(slug))
        except:
            quiz = None
        if quiz is not None:
            message = 'Quiz Found'
            mcqs = MCQuestion.objects.all().order_by('id')
            prgs = Problem.objects.all().order_by('id')
            regiter_count = quiz.participants.count()
            # 1.Form to add MCQ to quiz
            # 2.Form to add Problems to quiz
            # 3.Quiz stats
            return render_to_response('quiz_dashboard.html', locals(), context_instance=RequestContext(request))
        else:
            message = 'Quiz Does not exist'
            return render_to_response('quiz_dashboard.html', locals(), context_instance=RequestContext(request))
    else:
        message = '404'
        return render_to_response('404.html', locals(), context_instance=RequestContext(request))

