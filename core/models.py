#!/usr/bin/env python
# encoding: utf-8

from django.db.models import *
from django.dispatch import receiver
from django.template.defaultfilters import slugify

class Question(Model):
    title = CharField(max_length=80, null=False,
        verbose_name=u'Titulo'
    )
    slug = SlugField(max_length=80, null=False, unique=True)
    description = TextField(null=True, blank=True,
        verbose_name=u'Descrição'
    )
    views = IntegerField(default=0)

    class Meta:
        db_table = u'question'

    def __unicode__(self):
        return u"%s" % (self.title)

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

    def increment_view(self):
        self.views += 1
        self.save()

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


@receiver(signals.pre_save, sender=Question)
def generate_slug(sender, instance, signal=None, **kwargs):
    instance.slug = slugify(instance.title)
    dups = sender.objects.filter(slug=instance.slug)\
                         .exclude(pk=instance.pk).count()
    instance.slug += '-' + str(dups) if dups else ''
