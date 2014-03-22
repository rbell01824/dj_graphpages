#!/usr/bin/env python
# coding=utf-8

""" Some description here

3/15/14 - Initial creation

"""

from __future__ import unicode_literals
import logging

log = logging.getLogger(__name__)

__author__ = 'richabel'
__date__ = '3/15/14'
__license__ = "All rights reserved"
__version__ = "0.1"
__status__ = "dev"

from django.contrib import admin

from taggit.admin import TaggedItemInline
from taggit_suggest.models import TagKeyword, TagRegex
from taggit.models import Tag


class TagKeywordInline(admin.StackedInline):
    model = TagKeyword


class TagRegxInline(admin.StackedInline):
    model = TagRegex


class TagSuggestAdmin(admin.ModelAdmin):
    inlines = [
        TaggedItemInline,
        TagKeywordInline,
        TagRegxInline,
    ]
    # suit_form_tabs = (('general', 'General'),
    #                   ('form', 'Form'),
    #                   ('formpage', 'Form Page'),
    #                   ('query', 'Query'),
    #                   ('graphpage', 'Graph Page')
    #                   )
# admin.site.unregister(Tag)
admin.site.register(Tag, TagSuggestAdmin)
