#!/usr/bin/env python
# encoding: utf-8

from django.template import Context, Library
register = Library()

@register.inclusion_tag('date_badge.html')
def date_badge(date, action="Posted"):
    return {
        'date': date,
        'action': action,
    }
