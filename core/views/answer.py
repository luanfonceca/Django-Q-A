#!/usr/bin/env python
# encoding: utf-8

from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from url_decorator import url
from core.models import *
from core.forms import *

@url(regex=r'^question/(?P<slug>[\w-]+)\
             /answer/add/?$',
     name="answer_add")
def add(request, slug):
    question = Question.objects.get(slug=slug)
    answer_form = AnswerForm(request.POST or None)
    if answer_form.is_valid():
        answer_form.save(question)
    return redirect('question', slug)


@url(regex=r'^question/(?P<slug>[\w-]+)\
             /answer/edit/(?P<answer_pk>\d+)/?$',
     name="answer_edit")
def edit(request, slug, answer_pk):
    question = Question.objects.get(slug=slug)
    answer = Answer.objects.get(pk=answer_pk)
    answer_form = AnswerForm(
        data=request.POST or None,
        instance=answer
    )
    if answer_form.is_valid():
        answer_form.save(question)
    return redirect('question', slug)


@url(regex=r'^question/(?P<slug>[\w-]+)\
             /answer/delete/(?P<answer_pk>\d+)/?$',
     name="answer_delete")
def delete(request, slug, answer_pk):
    answer = Answer.objects.get(pk=answer_pk)
    if request.method == 'POST':
        answer.delete()
    return redirect('question', slug)


@url(regex=r'^question/(?P<slug>[\w-]+)\
             /answer/set/correct/(?P<answer_pk>\d+)/?$',
     name="answer_set_as_correct")
def set_as_correct(request, slug, answer_pk):
    answer = Answer.objects.get(pk=answer_pk)
    if request.method == 'POST':
        answer.set_as_correct()
    return redirect('question', slug)


@url(regex=r'^question/(?P<slug>[\w-]+)\
             /answer/aprove/(?P<answer_pk>\d+)/?$',
     name="answer_aprove")
def aprove(request, slug, answer_pk):
    answer = Answer.objects.get(pk=answer_pk)
    answer.increment_aproves()
    return redirect('question', slug)


@url(regex=r'^question/(?P<slug>[\w-]+)\
             /answer/desaprove/(?P<answer_pk>\d+)/?$',
     name="answer_desaprove")
def desaprove(request, slug, answer_pk):
    answer = Answer.objects.get(pk=answer_pk)
    answer.increment_desaproves()
    return redirect('question', slug)
