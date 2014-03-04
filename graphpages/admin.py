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

import uuid
import copy

# from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.forms import SelectMultiple
from django.db import models
# from django.utils.text import slugify
from django.forms import Textarea, TextInput
from django.contrib import admin
from django import forms

from suit.widgets import AutosizedTextarea

from .models import GraphPageTags, GraphPage
from .models import GraphTemplateTags, GraphTemplates
from .models import Graph2Tags, Graph2Form, Graph2Template, Graph2Graph, Graph2Query
from .models import Graph3Graph


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
    ordering = ('name',)
    save_on_top = True
    actions = ['delete_selected', 'duplicate_records']
    pass

    # noinspection PyMethodMayBeStatic
    def tags_list(self, obj):
        rtn = ''
        for tag in obj.tags.all():
            rtn += '; ' + tag.tag
        return rtn[1:]

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def duplicate_records(self, request, queryset):
        for obj in queryset:
            obj.id = None
            obj.name += '_dup'
            obj.save()

    duplicate_records.short_description = "Duplicate selected records"


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
    actions = ['delete_selected', 'duplicate_records', 'graph_admin_action']
    pass

    # noinspection PyMethodMayBeStatic
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

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def duplicate_records(self, request, queryset):
        for obj in queryset:
            obj.id = None
            obj.name += '_dup'
            obj.save()

    duplicate_records.short_description = "Duplicate selected records"


admin.site.register(GraphPage, GraphPageAdmin)

#
###############################################################################
#
# GraphPage2: improved models
#
###############################################################################
#


class Graph2TagsAdmin(admin.ModelAdmin):
    model = Graph2Tags
    search_fields = ('tag', 'description')
    list_display = ('tag_edit', 'tag', 'description',)
    fields = ('tag', 'description')
    list_editable = ('tag',)
    save_on_top = True
    pass

    # noinspection PyMethodMayBeStatic
    def tag_edit(self, obj):
        return 'Edit ' + obj.tag
admin.site.register(Graph2Tags, Graph2TagsAdmin)


class Graph2FormAdmin(admin.ModelAdmin):
    model = Graph2Form
    search_fields = ('name', 'description')
    list_display = ('name', 'tags_list', 'description', 'form',)
    fields = (('name', 'description', 'tags',),
              'form')
    filter_horizontal = ('tags',)
    # formfield_overrides = {models.ManyToManyField: {'widget': SelectMultiple(attrs={'size': '10'})}, }
    ordering = ('name',)
    save_on_top = True
    actions = ['delete_selected', 'duplicate_records']
    pass

    # noinspection PyMethodMayBeStatic
    def tags_list(self, obj):
        rtn = ''
        for tag in obj.tags.all():
            rtn += '; ' + tag.tag
        return rtn[1:]

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def duplicate_records(self, request, queryset):
        for obj in queryset:
            obj.id = None
            obj.name += '_dup'
            obj.save()
    duplicate_records.short_description = "Duplicate selected records"

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'name':
            kwargs['widget'] = TextInput(attrs={'size': '140'})
        if db_field.name == 'description':
            kwargs['widget'] = Textarea(attrs={'rows': '3', 'cols': '140'})
        if db_field.name == 'form':
            kwargs['widget'] = Textarea(attrs={'rows': '10', 'cols': '140'})
        return super(Graph2FormAdmin, self).formfield_for_dbfield(db_field, **kwargs)
admin.site.register(Graph2Form, Graph2FormAdmin)


class Graph2TemplateAdmin(admin.ModelAdmin):
    model = Graph2Template
    search_fields = ('name', 'description')
    list_display = ('name', 'tags_list', 'description', 'template',)
    fields = (('name', 'description', 'tags',),
              'template')
    filter_horizontal = ('tags',)
    # formfield_overrides = {models.ManyToManyField: {'widget': SelectMultiple(attrs={'size': '10'})}, }
    ordering = ('name',)
    save_on_top = True
    actions = ['delete_selected', 'duplicate_records']
    pass

    # noinspection PyMethodMayBeStatic
    def tags_list(self, obj):
        rtn = ''
        for tag in obj.tags.all():
            rtn += '; ' + tag.tag
        return rtn[1:]

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def duplicate_records(self, request, queryset):
        for obj in queryset:
            obj.id = None
            obj.name += '_dup'
            obj.save()
    duplicate_records.short_description = "Duplicate selected records"

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'name':
            kwargs['widget'] = TextInput(attrs={'size': '140'})
        if db_field.name == 'description':
            kwargs['widget'] = Textarea(attrs={'rows': '3', 'cols': '140'})
        if db_field.name == 'template':
            kwargs['widget'] = Textarea(attrs={'rows': '10', 'cols': '140'})
        return super(Graph2TemplateAdmin, self).formfield_for_dbfield(db_field, **kwargs)

admin.site.register(Graph2Template, Graph2TemplateAdmin)


class Graph2QueryAdmin(admin.ModelAdmin):
    model = Graph2Query
    search_fields = ('name', 'description')
    list_display = ('name', 'tags_list', 'description', 'query',)
    fields = (('name', 'description', 'tags',),
              'query')
    filter_horizontal = ('tags',)
    # formfield_overrides = {models.ManyToManyField: {'widget': SelectMultiple(attrs={'size': '10'})}, }
    ordering = ('name',)
    save_on_top = True
    actions = ['delete_selected', 'duplicate_records']
    pass

    # noinspection PyMethodMayBeStatic
    def tags_list(self, obj):
        rtn = ''
        for tag in obj.tags.all():
            rtn += '; ' + tag.tag
        return rtn[1:]

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def duplicate_records(self, request, queryset):
        for obj in queryset:
            obj.id = None
            obj.name += '_dup'
            obj.save()
    duplicate_records.short_description = "Duplicate selected records"

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'name':
            kwargs['widget'] = TextInput(attrs={'size': '140'})
        if db_field.name == 'description':
            kwargs['widget'] = Textarea(attrs={'rows': '3', 'cols': '140'})
        if db_field.name == 'query':
            kwargs['widget'] = Textarea(attrs={'rows': '10', 'cols': '140'})
        return super(Graph2QueryAdmin, self).formfield_for_dbfield(db_field, **kwargs)

admin.site.register(Graph2Query, Graph2QueryAdmin)

###############################################################################


class Graph2GraphAdmin(admin.ModelAdmin):
    model = Graph2Graph

    # noinspection PyMethodMayBeStatic
    def display_graph(self, obj):
        rtn = u"<div><a class='btn btn-primary btn-sm' href='/graphpages/graph2/%s'>Display</a></div>" % obj.id
        return rtn
    display_graph.short_description = ''
    display_graph.allow_tags = True

    search_fields = ('name', 'description')
    readonly_fields = ('form_current_value', 'template_current_value', 'query_current_value')
    list_display = ('display_graph', 'name', 'tags_list', 'description',
                    'form', 'template', 'query')
    fieldsets = ((None, {'fields': (('name',
                                     'form_current_value',
                                     'template_current_value',
                                     'query_current_value',
                                     'tags',))}),
                 ('Description', {
                     'classes': ('collapse',),
                     'fields': ('description',)}),
                 ('Form', {
                     'classes': ('collapse',),
                     'fields': ('form',)}),
                 ('Template', {
                     'classes': ('collapse',),
                     'fields': ('template',)}),
                 ('Query', {
                     'classes': ('collapse',),
                     'fields': ('query',)}),
                 )
    list_display_links = ('name',)
    filter_horizontal = ('tags',)
    save_on_top = True
    ordering = ('name',)
    actions = ['delete_selected', 'duplicate_records', 'graph_admin_action']
    pass

    # noinspection PyMethodMayBeStatic
    def tags_list(self, obj):
        rtn = ''
        for tag in obj.tags.all():
            rtn += '; ' + tag.tag
        return rtn[1:]

    # noinspection PyMethodMayBeStatic
    def form_current_value(self, obj):
        return 'Form: ' + obj.form.name

    # noinspection PyMethodMayBeStatic
    def template_current_value(self, obj):
        return 'Template: ' + obj.template.name

    # noinspection PyMethodMayBeStatic
    def query_current_value(self, obj):
        return 'Query: ' + obj.query.name

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def duplicate_records(self, request, queryset):
        for obj in queryset:
            obj.id = None
            obj.name += '_dup'
            obj.save()
    duplicate_records.short_description = "Duplicate selected records"

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'name':
            kwargs['widget'] = TextInput(attrs={'size': '140'})
        if db_field.name == 'description':
            kwargs['widget'] = Textarea(attrs={'rows': '5', 'cols': '120'})
        return super(Graph2GraphAdmin, self).formfield_for_dbfield(db_field, **kwargs)

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def graph_admin_action(self, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        # r = selected[0]
        #noinspection PyUnusedLocal
        # ct = ContentType.objects.get_for_model(queryset.model)
        return HttpResponseRedirect("/graphpages/graph2/%s" % (selected[0]))
    graph_admin_action.short_description = 'Display graph'


admin.site.register(Graph2Graph, Graph2GraphAdmin)


#
###############################################################################
#
# GraphPage3: improved models
#
###############################################################################
#

# todo: do form like this: https://github.com/darklow/django-suit-examples/blob/master/admin.py
class Graph3GraphAdmin(admin.ModelAdmin):

    # noinspection PyMethodMayBeStatic
    def display_graph(self, obj):
        rtn = u"<div><a class='btn btn-primary btn-sm' href='/graphpages/graph3/%s'>Display</a></div>" % obj.id
        return rtn
    display_graph.short_description = ''
    display_graph.allow_tags = True

    model = Graph3Graph
    search_fields = ('name', 'description')
    readonly_fields = ('form_slug', 'query_slug', 'template_slug')
    list_display = ('display_graph', 'name', 'tags_slug', 'description',
                    'form_slug', 'query_slug', 'template_slug'
                    )
    fieldsets = ((None, {'fields': ('name', 'description', 'tags',)}),
                 ('Form', {
                     'classes': ('full-width',),
                     'fields': ('form',)}),
                 ('Graph Page', {
                     'classes': ('full-width',),
                     'fields': ('template',)}),
                 )
    list_display_links = ('name',)
    filter_horizontal = ('tags',)
    save_on_top = True
    ordering = ('name',)
    actions = ['delete_selected', 'duplicate_records', 'graph_admin_action']
    SLUG_LEN = 20
    pass

    # noinspection PyMethodMayBeStatic
    def tags_slug(self, obj):
        """
        Make list of tags seperated by ';'
        """
        rtn = ''
        for tag in obj.tags.all():
            rtn += '; ' + tag.tag
        return rtn[1:]

    # noinspection PyMethodMayBeStatic
    def form_slug(self, obj):
        """
        Generate form text for list display
        """
        return obj.form[:min(self.SLUG_LEN, len(obj.form))]

    # noinspection PyMethodMayBeStatic
    def query_slug(self, obj):
        return obj.query[:min(self.SLUG_LEN, len(obj.query))]

    # noinspection PyMethodMayBeStatic
    def template_slug(self, obj):
        return obj.template[:min(self.SLUG_LEN, len(obj.template))]

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'name':
            kwargs['widget'] = TextInput(attrs={'class': 'span12', 'size': '140'})
        if db_field.name == 'description':
            kwargs['widget'] = Textarea(attrs={'class': 'span12', 'rows': '2', 'cols': '140'})
        if db_field.name == 'form':
            kwargs['widget'] = Textarea(attrs={'class': 'span12', 'rows': '10', 'cols': '140'})
        if db_field.name == 'query':
            kwargs['widget'] = Textarea(attrs={'class': 'span12', 'rows': '3', 'cols': '140'})
        if db_field.name == 'template':
            kwargs['widget'] = Textarea(attrs={'class': 'span12', 'rows': '10', 'cols': '140'})
        return super(Graph3GraphAdmin, self).formfield_for_dbfield(db_field, **kwargs)

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def duplicate_records(self, request, queryset):
        """
        Duplicate the selected records
        """
        for obj in queryset:
            newobj = copy.deepcopy(obj)
            newobj.id = None
            newobj.name += uuid.uuid1().hex
            newobj.save()
            # noinspection PyStatementEffect
            newobj.tags.add(*obj.tags.all())
    duplicate_records.short_description = "Duplicate selected records"

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def graph_admin_action(self, request, queryset):
        """
        Display this graph
        """
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        # r = selected[0]
        #noinspection PyUnusedLocal
        # ct = ContentType.objects.get_for_model(queryset.model)
        return HttpResponseRedirect("/graphpages/3raph3/%s" % (selected[0]))
    graph_admin_action.short_description = 'Display graph'
admin.site.register(Graph3Graph, Graph3GraphAdmin)
