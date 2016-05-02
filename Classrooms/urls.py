from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from challenges.views import QuizListView
from mcqs.views import MCQListView

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'CodeChamps.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^$', 'person.views.home', name='home'),


                       # ####DEVELOPER URLS
                       url(r'^register/$', 'person.views.register'),
                       url(r'^login/$', 'person.views.loginRequest'),
                       url(r'^logout/$', 'person.views.logoutRequest'),
                       url(r'^profile/(?P<username>.*)/$', 'person.views.profile'),
                       (r'^uploadprofilepic/$', 'person.views.upload_profile_pic'),
                       (r'^removeprofilepic/$', 'person.views.remove_profile_pic'),
                       (r'^reset/$', 'person.views.reset_password'),
                       (r'^settings/$', 'person.views.settings'),
                       (r'^updateprofile/$', 'person.views.update_profile'),
                       (r'^changepassword/$', 'person.views.password_change'),
                       (r'^user/activate/(?P<activation_key>\w+)/$', 'person.views.activation_view'),

                       # ##Problem URLS
                       (r'^problems/add_problem/$', 'Problems.views.add_problems'),
                       (r'^problems/list_problems/$', 'Problems.views.list_problems'),
                       (r'^problems/modify/(?P<problem_id>[0-9])$', 'Problems.views.modify_problem'),
                       (r'^practise$', 'Problems.views.all_problems'),
                       (r'^problems/solve/(?P<problem_id>[0-9])$', 'Problems.views.problem_page'),
                       (r'^get/program/(?P<slug>\d)/$','Problems.views.get_program'),

                       # ## Submission URLS
                       (r'^submit/$', 'Submissions.views.accept_submission'),
                       (r'^trial_submit/$', 'Submissions.views.trial_submission'),
                       (r'^submissions/(?P<problem_id>\d+)/(?P<submission_id>\d+)/(?P<file_number>\d+)$',
                        'Submissions.views.read_submission'),


                       # QuizTake
                       # url(r'^quiz/(?P<quiz>[-_\w]+)/(?P<username>[-_\w]+)/$', mcqs.views.quiz_take, name='quiz_take'),
                       url(r'^challenges/$', QuizListView.as_view(), name='quiz_list'),
                       url(r'^challenges/(?P<quiz>[-_\w]+)/$', 'challenges.views.quiz_take', name='quiz_take'),
                       url(r'^register/(?P<quiz_id>\d)/$', 'challenges.views.register'),
                       url(r'^start/(?P<quiz_id>\d)/$', 'challenges.views.start_quiz'),
                       url(r'^end/(?P<quiz_id>\d)/$', 'challenges.views.exit_quiz'),
                       url(r'^add_quiz/$','challenges.views.add_quiz',name='Add Quiz'),
                       url(r'^quiz_dashboard/(?P<slug>\d)/$', 'challenges.views.quiz_dashboard'),
                       # MCQURLS
                       url(r'^mcqs/(?P<slug>\d)/$', 'mcqs.views.get_mcq', name='mcq_detail'),
                       url(r'^checkans/(?P<slug>\d)/$', 'mcqs.views.accept_answer', name='check_answer'),
                       url(r'^mcqs/$', MCQListView.as_view(), name='mcq_list'),

                       #college autocomplete url
                       url(r'^get_colleges/$','college.views.get_colleges',name='get_college'),
                       url(r'^college/$','college.views.home',name='college_home')

)+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)