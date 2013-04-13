#!/usr/bin/env python
# encoding: utf-8

from django.forms import *

from core.models import *

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        exclude = ['slug', 'views']

class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        exclude = ['is_correct', 'aproves',
                   'desaproves', 'question']
