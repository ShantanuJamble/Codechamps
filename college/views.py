import json
import datetime
from django.http import HttpResponse
from django.shortcuts import render, render_to_response

# Create your views here.
from django.template import RequestContext
from challenges.forms import AddQuizForm
from college.models import College


def get_colleges(request):
    if request.is_ajax():
        start = request.GET.get('term', '')
        college_list = College.objects.all().filter(name__startswith=start)[:5]
        results = []
        for clg in college_list:
            clg_json = {}
            clg_json['id'] = clg.id
            clg_json['label'] = clg.name
            clg_json['value'] = clg.name
            results.append(clg_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def home(request):
    form = AddQuizForm()
    if request.method == 'POST':
        form = AddQuizForm(request.POST)
        print form.is_valid()
        request_dict = request.POST.get('date_time')
        print (request_dict)
        request_dict = datetime.datetime.strptime(request_dict, '%Y-%m-%d %H:%M:%S')
        print request_dict
        print type(request_dict)
        request_dict = request.POST.get('date')
        print type(request_dict)
        request_dict = request.POST.get('time')
        print type(request_dict)
        if form.is_valid():
            d = 'asf'
            # print d
            #print type(d)
    return render_to_response('college_list.html', {'form': AddQuizForm}, context_instance=RequestContext(request))
