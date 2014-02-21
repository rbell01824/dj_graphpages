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
# from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.forms import SelectMultiple
from django.db import models


class GraphTemplateTagsAdmin(admin.ModelAdmin):
    model = GraphTemplateTags
    search_fields = ('tag', 'description')
    list_display = ('tag', 'description')
    fields = ('tag', 'description')
    # list_editable = ('description',)
    save_on_top = True
    pass
admin.site.register(GraphTemplateTags, GraphTemplateTagsAdmin)


class GraphTemplatesAdmin(admin.ModelAdmin):
    model = GraphTemplates
    search_fields = ('name', 'description')
    list_display = ('name', 'tags_list', 'description', 'template',)
    fields = (('name', 'description', 'tags',),
              'template')
    formfield_overrides = {models.ManyToManyField: {'widget': SelectMultiple(attrs={'size': '10'})}, }
    save_on_top = True
    pass

    def tags_list(self, obj):
        rtn = ''
        for tag in obj.tags.all():
            rtn += '; ' + tag.tag
        return rtn[1:]
admin.site.register(GraphTemplates, GraphTemplatesAdmin)


class GraphPageTagsAdmin(admin.ModelAdmin):
    model = GraphPageTags
    search_fields = ('tag', 'description')
    list_display = ('tag', 'description',)
    fields = ('tag', 'description')
    # list_editable = ('description',)
    save_on_top = True
    pass
admin.site.register(GraphPageTags, GraphPageTagsAdmin)


class GraphPageAdmin(admin.ModelAdmin):
    model = GraphPage
    search_fields = ('name', 'description')
    list_display = ('name', 'tags_list', 'description',
                    'form', 'template', 'page', 'query')
    fieldsets = ((None, {'fields': (('name', 'tags', 'description',),
                                    'template', 'query')}),
                 ('Advanced options', {
                     'classes': ('collapse',),
                     'fields': (('page_format', 'page'),
                                'form')}))
    formfield_overrides = {models.ManyToManyField: {'widget': SelectMultiple(attrs={'size': '10'})}, }
    save_on_top = True
    ordering = ('name',)
    actions = ['delete_selected', 'graph_admin_action']
    pass

    def tags_list(self, obj):
        rtn = ''
        for tag in obj.tags.all():
            rtn += '; ' + tag.tag
        return rtn[1:]

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def graph_admin_action(self, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        # r = selected[0]
        #noinspection PyUnusedLocal
        # ct = ContentType.objects.get_for_model(queryset.model)
        return HttpResponseRedirect("/graphpages/graph/%s" % (selected[0]))
    graph_admin_action.short_description = 'Display graph'
admin.site.register(GraphPage, GraphPageAdmin)
