#!/usr/bin/env python
# encoding: utf-8

from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from url_decorator import url
from core.models import *
from core.forms import *


@url(r'^/?$', name="questions")
def list(request):
    data = {
        'questions': Question.objects.all()
    }
    return render_to_response('question/list.html', data,
        context_instance=RequestContext(request))


@url(r'^question/add/?$', name="question_add")
def add(request):
    question_form = QuestionForm(request.POST or None)

    if question_form.is_valid():
        question_form.save()
        return redirect('questions')

    data = {
        'question_form': question_form,
    }
    return render_to_response('question/add.html', data,
        context_instance=RequestContext(request))


@url(r'^question/edit/(?P<slug>[\w-]+)/?$', name="question_edit")
def edit(request, slug):
    question = Question.objects.get(slug=slug)
    question_form = QuestionForm(data=request.POST or None,
        instance=question
    )

    if question_form.is_valid():
        question_form.save()
        return redirect('questions')

    data = {
        'question': question,
        'question_form': question_form
    }
    return render_to_response('question/edit.html', data,
        context_instance=RequestContext(request))


@url(r'^question/delete/(?P<slug>[\w-]+)/?$', name="question_delete")
def delete(request, slug):
    question = Question.objects.get(slug=slug)

    if request.method == 'POST':
        question.delete()
        return redirect('questions')

    data = {
        'question': question,
        'question_form': question_form
    }
    return render_to_response('question/delete.html', data,
        context_instance=RequestContext(request))

@url(r'^question/(?P<slug>[\w-]+)/?$', name="question")
def view(request, slug):
    question = Question.objects.get(slug=slug)
    question.increment_view()

    data = {
        'question': question,
    }
    return render_to_response('question/view.html', data,
        context_instance=RequestContext(request))