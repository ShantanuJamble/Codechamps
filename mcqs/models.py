from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _
# Create your models here.
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible
from model_utils.managers import InheritanceManager
from Problems.models import Problem
from challenges.models import QuizModel, Category

ANSWER_ORDER_OPTIONS = (
    ('content', _('Content')),
    ('random', _('Random')),
    ('none', _('None'))
)


class Question(models.Model):
    """docstring for Question"""
    content = models.CharField(max_length=1000,
                               blank=False,
                               help_text=_("Enter the question text that "
                                           "you want displayed"),
                               verbose_name=_('Question'))
    explanation = models.TextField(max_length=2000,
                                   blank=True,
                                   help_text=_("Explanation to be shown "
                                               "after the question has "
                                               "been answered."),
                                   verbose_name=_('Explanation'))
    quiz = models.ManyToManyField(QuizModel, blank=True, null=True)
    category = models.ForeignKey(Category, null=True)
    marks = models.IntegerField(blank=False, null=False, default=1)
    objects = InheritanceManager()

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")
        ordering = ['category']

    def __str__(self):
        return self.content


class MCQuestion(Question):
    answer_order = models.CharField(
        max_length=30, null=True, blank=True,
        choices=ANSWER_ORDER_OPTIONS,
        help_text=_("The order in which multichoice "
                    "answer options are displayed "
                    "to the user"),
        verbose_name=_("Answer Order"))

    def check_if_correct(self, guess):
        answer = ''
        try:
            answer = self.get_answers()
            answer = answer.get(content=guess)
        except Answer.DoesNotExist:
            print Answer.DoesNotExist
        if answer.correct is True:
            return True
        else:
            return False

    def get_answers_count(self):
        return Answer.objects.filter(question=self).count()

    def get_correct_ans(self):
        answer = Answer.objects.filter(question=self)
        for ans in answer:
            if ans.correct is True:
                return ans

    def order_answers(self, queryset):
        if self.answer_order == 'content':
            return queryset.order_by('content')
        if self.answer_order == 'random':
            return queryset.order_by('?')
        if self.answer_order == 'none':
            return queryset.order_by()
        else:
            return queryset.order_by()

    def get_answers(self):
        return self.order_answers(Answer.objects.filter(question=self))

    def get_answers_list(self):
        return [(answer.id, answer.content) for answer in
                self.order_answers(Answer.objects.filter(question=self))]

    def answer_choice_to_string(self, guess):
        return Answer.objects.get(id=guess).content

    def get_absolute_url(self):
        return '/mcqs/' + str(self.id) + '/'

    class Meta:
        verbose_name = _("Multiple Choice Question")
        verbose_name_plural = _("Multiple Choice Questions")


@python_2_unicode_compatible
class Answer(models.Model):
    question = models.ForeignKey(MCQuestion, verbose_name=_("Question"))

    content = models.CharField(max_length=1000,
                               blank=False,
                               help_text=_("Enter the answer text that "
                                           "you want displayed"),
                               verbose_name=_("Content"))

    correct = models.BooleanField(blank=False,
                                  default=False,
                                  help_text=_("Is this a correct answer?"),
                                  verbose_name=_("Correct"))

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = _("Answer")
        verbose_name_plural = _("Answers")


class SittingManager(models.Manager):
    def format_string(self, answers_set, question_set, programs_set):
        if len(question_set) != 0:
            question_set = question_set.encode('ascii')
            question_set = list(question_set)
            question_set[- 1] = ''
            question_set = ''.join(question_set)
        else:
            question_set = None
        if len(answers_set) != 0:
            answers_set = answers_set.encode('ascii')
            answers_set = list(answers_set)
            answers_set[- 1] = ''
            answers_set = ''.join(answers_set)
        else:
            answers_set = None
        if len(programs_set) != 0:
            programs_set = programs_set.encode('ascii')
            programs_set = list(programs_set)
            programs_set[-1] = ''
            programs_set = ''.join(programs_set)
        else:
            programs_set = None
        return answers_set, question_set, programs_set

    def new_sitting(self, user, quiz):
        if quiz.random_order is True:
            questions = MCQuestion.objects.all().filter(quiz=quiz).order_by('?')
            programs = Problem.objects.all().filter(quiz=quiz).order_by('?')
        else:
            questions = MCQuestion.objects.all().filter(quiz=quiz).order_by('id')
            programs = Problem.objects.all().filter(quiz=quiz).order_by('id')
        print questions
        print len(programs)
        question_set = ''
        answers_set = ''
        programs_set = ''
        for question in questions:
            question_set = question_set + str(question.id) + ','
            answers_set = answers_set + str(0) + ','
        for prg in programs:
            programs_set = programs_set + str(prg.id) + ','
        answers_set, question_set, programs_set = self.format_string(answers_set, question_set, programs_set)
        # print answers_set, question_set
        new_sitting = self.create(user=user,
                                  quiz=quiz,
                                  question_order=question_set,
                                  answers_set=answers_set,
                                  programs=programs_set
        )
        return new_sitting

    def user_sitting(self, user, quiz):
        # if you want to allow only one chance to user
        if quiz.single_attempt is True and self.filter(user=user, quiz=quiz, complete=True).exists():
            return False
        try:
            sitting = self.get(user=user, quiz=quiz)
        except Sitting.DoesNotExist:
            sitting = self.new_sitting(user, quiz)
        except Sitting.MultipleObjectsReturned:
            sitting = self.filter(user=user, quiz=quiz, complete=False)[0]
        return sitting


@python_2_unicode_compatible
class Sitting(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, null=False, verbose_name="User")

    quiz = models.ForeignKey(QuizModel, blank=False, null=False, verbose_name="Quiz")
    # for actual order
    question_order = models.CommaSeparatedIntegerField(max_length=1024, blank=True, null=True,
                                                       verbose_name="Questions_Order")

    programs = models.CommaSeparatedIntegerField(max_length=1024, blank=True, null=True,
                                                 verbose_name="Programs")
    # Has Quiz been completed
    complete = models.BooleanField(default=False, blank=False, verbose_name=_("Complete"))

    # Answers by user
    answers_set = models.CommaSeparatedIntegerField(max_length=1024, default=None, blank=True,
                                                    verbose_name="User's Answers")

    # Score

    score = models.PositiveIntegerField(default=0, blank=False, null=False, verbose_name="Score")

    start_time = models.DateTimeField(help_text="Participant Start Time", blank=False, null=True, default=None)
    end_time = models.DateTimeField(help_text="Participant End Time", blank=False, null=True, default=None)
    objects = SittingManager()

    def __str__(self):
        return str(self.id)