#!/usr/bin/env python
# encoding: utf-8

from django.db.models import *
from django.dispatch import receiver
from django.template.defaultfilters import slugify

class Question(Model):
    author = CharField(max_length=80, null=False,
        verbose_name=u'Autor'
    )
    title = CharField(max_length=80, null=False,
        verbose_name=u'Titulo'
    )
    slug = SlugField(max_length=80, null=False, unique=True)
    description = TextField(null=True, blank=True,
        verbose_name=u'Descrição'
    )
    views = IntegerField(default=0)
    create_at = DateTimeField(null=False, auto_now_add=True)

    class Meta:
        db_table = u'question'

    def __unicode__(self):
        return u"#%s, %s: %s" % (
            self.pk, self.author, self.title
        )

    @permalink
    def get_absolute_url(self):
        return 'question', (), {
            'slug': self.slug,
        }

    @permalink
    def get_edit_url(self):
        return 'question_edit', (), {
            'slug': self.slug,
        }

    @permalink
    def get_delete_url(self):
        return 'question_delete', (), {
            'slug': self.slug,
        }

    @permalink
    def get_answer_add_url(self):
        return 'answer_add', (), {
            'slug': self.slug,
        }

    def increment_view(self):
        self.views += 1
        self.save()

class Answer(Model):
    author = CharField(max_length=80, null=False,
        verbose_name=u'Autor'
    )
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
        ordering = ['-aproves', 'desaproves', 'pk']

    def __unicode__(self):
        return u"#%s, %s: %s" % (
            self.pk, self.author, self.body
        )

    @permalink
    def get_edit_url(self):
        return 'answer_edit', (), {
            'slug': self.question.slug,
            'answer_pk': self.pk,
        }

    @permalink
    def get_set_as_correct_url(self):
        return 'answer_set_as_correct', (), {
            'slug': self.question.slug,
            'answer_pk': self.pk,
        }

    @permalink
    def get_aprove_url(self):
        return 'answer_aprove', (), {
            'slug': self.question.slug,
            'answer_pk': self.pk
        }

    @permalink
    def get_desaprove_url(self):
        return 'answer_desaprove', (), {
            'slug': self.question.slug,
            'answer_pk': self.pk
        }

    def set_as_correct(self):
        self.is_correct = True
        self.aproves += 100
        self.save()

    def increment_aproves(self):
        self.aproves += 1
        self.save()

    def increment_desaproves(self):
        self.desaproves += 1
        self.save()


# Signals
@receiver(signals.pre_save, sender=Question)
def generate_slug(sender, instance, signal=None, **kwargs):
    instance.slug = slugify(instance.title)
    dups = sender.objects.filter(slug=instance.slug)\
                         .exclude(pk=instance.pk).count()
    instance.slug += '-' + str(dups) if dups else ''
