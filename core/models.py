#!/usr/bin/env python
# encoding: utf-8

from django.db.models import *

class Question(Model):
    title = CharField(max_length=80, null=False,
        verbose_name=u'Titulo'
    )
    slug = CharField(max_length=80, null=False)
    description = TextField(null=True, blank=True,
        verbose_name=u'Descrição'
    )
    views = IntegerField(default=0)

    class Meta:
        db_table = u'question'

    def __unicode__(self):
        return "%s" % (self.title)


class Answer(Model):
    body = TextField(null=False, verbose_name=u'Resposta')
    is_correct = BooleanField(null=False, default=False)
    create_at = DateTimeField(null=False, auto_now_add=True)
    aproves = IntegerField(default=0)
    desaproves = IntegerField(default=0)

    # relations
    question = ForeignKey(Question, null=True, related_name='answers',
        on_delete=CASCADE
    )

    class Meta:
        db_table = u'answer'

    def __unicode__(self):
        return "%s" % (self.body)


class Reply(Model):
    body = TextField(null=False, verbose_name=u'Resposta')
    create_at = DateTimeField(null=False, auto_now_add=True)
    aproves = IntegerField(default=0)
    desaproves = IntegerField(default=0)

    # relations
    answer = ForeignKey(Answer, null=True, related_name='replies',
        on_delete=CASCADE
    )

    class Meta:
        db_table = u'reply'

    def __unicode__(self):
        return "%s" % (self.body)
