from django.contrib.auth.models import User
from django.shortcuts import render, render_to_response, HttpResponseRedirect, Http404
from django.template import RequestContext
from person.models import Person
from Problems.models import Problem
from Submissions.compilers import read_result
from Submissions.models import Submission
from .forms import SubmissionForm
from .compilers import process_submission, process_trial_submission
import os
# Create your views here.
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


def save_submission(problem_id, username, status, marks, lang_chosen):
    submission = Submission(problem_id=problem_id, person=username, status=status, marks=marks, memory_used=0.0,
                            lang_chosen=lang_chosen)
    submission.save()
    if status == 'AC':
        try:
            user = User.objects.get(username=username)
            person = Person.objects.get(user=user)
            solved_count = person.solved_count
            solved_count += 1
            person.solved_count = solved_count
            person.save()
        except Person.DoesNotExist:
            pass
    return


def accept_submission(request):
    form = SubmissionForm()
    if not request.user.is_authenticated():
        HttpResponseRedirect("/login/")
    try:
        form = SubmissionForm(request.POST)
    except form is None:
        form = None
    print form.is_valid()
    if form.is_valid():
        problem_id = form.cleaned_data['problem_id']
        source = form.cleaned_data['source']
        lang_chosen = form.cleaned_data['lang_chosen']
        problem = None
        try:
            problem = Problem.objects.get(id=problem_id)
        except Problem.DoesNotExist:
            problem = None
        status, marks, result = process_submission(request.user.username, problem.title.replace(' ', '_'), source,
                                                   lang_chosen, problem.test_time, problem.test_count)
        if status == 'CE':
            result = "<br>".join(result.split("\n"))
        if status != 'duplicate':
            save_submission(problem_id, request.user.username, status, marks, lang_chosen)
        return render_to_response('submission_result.html', {'status': status, 'marks': marks, 'result': result},
                                  context_instance=RequestContext(request))
    else:
        pass
    return HttpResponseRedirect('/')


def trial_submission(request):
    form = SubmissionForm()
    if not request.user.is_authenticated():
        HttpResponseRedirect("/login/")
    try:
        form = SubmissionForm(request.POST)
    except form is None:
        form = None
    print form.is_valid()
    if form.is_valid():
        problem_id = form.cleaned_data['problem_id']
        source = form.cleaned_data['source']
        lang_chosen = form.cleaned_data['lang_chosen']
        problem = None
        try:
            problem = Problem.objects.get(id=problem_id)
        except Problem.DoesNotExist:
            problem = None
        # print problem_id, source, lang_chosen, problem
        status, marks, result = process_trial_submission(request.user.username, problem.title.replace(' ', '_'), source,
                                                         lang_chosen, problem.test_time, problem.test_count)
        expected = None
        if status == 'CE':
            result = "<br>".join(result.split("\n"))
        if status is None:
            expected = "<br>".join(problem.output_sample.split("\n"))
            result = "<br>".join(result[0].split("\n"))
        return render_to_response('trial_submission_result.html',
                                  locals(),
                                  context_instance=RequestContext(request))
    else:
        pass
    return HttpResponseRedirect('/')


# returns Soltuion
def read_submission(request, problem_id, submission_id, file_number):
    try:
        user = User.objects.get(username=request.user.username)
        person = Person.objects.get(user=user)
        problem = Problem.objects.get(id=problem_id)
        problem_title = problem.title.replace(" ", "_")
        submission = Submission.objects.get(id=submission_id)
        lang_chosen = submission.lang_chosen
        status=submission.status
        marks=submission.marks
        file_name = 'Solution_' + str(file_number) + '.' + lang_chosen
        source_path = os.path.join(BASE_DIR, 'static', 'media', 'submissions', request.user.username, problem_title)
        solution = read_result(source_path, file_name)
        return render_to_response('submission.html', locals(),
                                  context_instance=RequestContext(request))
    except Problem.DoesNotExist:
        submission = 'Not Found'
        return render_to_response('submission.html', locals(),
                                  context_instance=RequestContext(request))
    return