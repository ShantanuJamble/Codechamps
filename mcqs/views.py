import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
# Create your views here.
from challenges.models import QuizModel
from challenges.views import quiz_dashboard
from mcqs.models import MCQuestion, Sitting
from person.models import Person


class MCQDetailView(DetailView):
    model = MCQuestion
    slug_field = 'id'
    context_object_name = 'question'

    def get_context_data(self, *args, **kwargs):
        context = super(MCQDetailView, self).get_context_data(**kwargs)
        return context


class MCQListView(ListView):
    model = MCQuestion


def get_mcq(request, slug):
    question = None
    sitting_id = request.POST.get('sitting_id')
    try:
        question = MCQuestion.objects.get(id=slug)
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
    options = question.get_answers()
    return render_to_response('mcqs/mcquestion_detail.html', locals(), context_instance=RequestContext(request))


def accept_answer(request, slug):
    marks = 0
    # import pdb
    # pdb.set_trace()
    print 'in accept ans'
    if request.method == 'POST':
        question = MCQuestion.objects.get(id=slug)
        user_answer = request.POST.get('choice')
        sitting_id = int(request.POST.get('sitting_id'))
        sitting = Sitting.objects.get(id=sitting_id)
        marks = int(sitting.score)
        question_set = list(sitting.question_order)  # [int(x) for x in sitting.question_order.split(',')]
        answer_set = list(sitting.answers_set)
        index = question_set.index(str(question.id))
        if question.check_if_correct(user_answer):
            print 1
            if answer_set[index] != '1':
                marks += 1
                answer_set[index] = '1'

        else:
            print 2
            if answer_set[index] == '1':
                marks -= 1
            else:
                print '*'
                marks = marks
            answer_set[index] = '0'
        sitting.answers_set = ''.join(answer_set)
        sitting.score = marks
        sitting.save()
    else:
        marks = marks
    # print marks
    jason_data = json.dumps({'marks': marks})
    return HttpResponse(jason_data, content_type="application/json")


# this method add question to a quiz
def add_mcqs(mcqs, quiz):
    for m in mcqs:
        q = MCQuestion.objects.get(id=int(m))
        q.quiz.add(quiz)
        try:
            q.save()
        except:
            print 'save failed'


def delete_mcqs(mcqs, quiz, all=False):
    all_mcqs = MCQuestion.objects.all()
    if not all:
        for q in all_mcqs:
            print str(q.id) not in mcqs and quiz in q.quiz.all()
            if str(q.id) not in mcqs and quiz in q.quiz.all():
                print 'in here for ' + q.content
                q.quiz.remove(quiz)
            try:
                q.save()
            except:
                print 'save failed'
    else:
        for q in all_mcqs:
            q.quiz.remove(quiz)
            try:
                q.save()
            except:
                print 'save failed'


def mcq_to_quiz(request):
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
        mcqs = []
        try:
            data = str(request.POST.getlist(u'mcqs'))
            print data
            for d in data:
                try:
                    i = int(d)
                    mcqs.append(d)
                except:
                    pass
            print(mcqs)
        except:
            mcqs = None
        print mcqs
        if mcqs:
            if str(request.GET['to_do']) == 'add':
                add_mcqs(mcqs, quiz)
            elif str(request.GET['to_do']) == 'delete':
                delete_mcqs(mcqs, quiz)
        else:
            delete_mcqs(mcqs, quiz, True)
        return HttpResponseRedirect('/quiz_dashboard/' + str(quiz.id))