#!/usr/bin/env python

"""

11/18/13 - Initial creation

"""

from __future__ import unicode_literals
import logging

log = logging.getLogger(__name__)

__author__ = 'rbell01824'
__date__ = '11/18/13'
__copyright__ = "Copyright 2013, Richard Bell"
__credits__ = ["rbell01824"]
__license__ = "All rights reserved"
__version__ = "0.1"
__maintainer__ = "rbell01824"
__email__ = "rbell01824@gmail.com"
__status__ = "dev"

from django.contrib import admin
from .models import GraphPageTags, GraphPage
from .models import GraphTemplateTags, GraphTemplates


class GraphTemplateTagsAdmin(admin.ModelAdmin):
    model = GraphTemplateTags
    search_fields = ('tag', 'description')
    list_display = ('tag', 'description')
    fields = ('tag', 'description')
    save_on_top = True
    pass


admin.site.register(GraphTemplateTags, GraphTemplateTagsAdmin)


class GraphTemplatesAdmin(admin.ModelAdmin):
    model = GraphTemplates
    search_fields = ('name', 'description')
    list_display = ('name', 'description', 'template')
    fields = (('name', 'description', 'tags',),
              'template')
    save_on_top = True
    pass


admin.site.register(GraphTemplates, GraphTemplatesAdmin)


class GraphPageTagsAdmin(admin.ModelAdmin):
    model = GraphPageTags
    search_fields = ('tag', 'description')
    list_display = ('tag', 'description')
    fields = ('tag', 'description')
    save_on_top = True
    pass


admin.site.register(GraphPageTags, GraphPageTagsAdmin)


class GraphPageAdmin(admin.ModelAdmin):
    model = GraphPage
    search_fields = ('name', 'description')
    list_display = ('name', 'description', 'form',
                    'template', 'page', 'query')
    fieldsets = ((None, {'fields': (('name', 'tags', 'description',),
                                    'template', 'query')}),
                 ('Advanced options', {
                     'classes': ('collapse',),
                     'fields': (('page_format', 'page'),
                                'form')}))
    save_on_top = True
    pass


admin.site.register(GraphPage, GraphPageAdmin)

