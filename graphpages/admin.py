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
from .models import Graph2Tags, Graph2Form, Graph2Template, Graph2Graph, Graph2Query
# from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.forms import SelectMultiple
from django.db import models
from django.utils.text import slugify
from django.forms import Textarea, TextInput


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

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'name':
            kwargs['widget'] = TextInput(attrs={'size': '140'})
        if db_field.name == 'description':
            kwargs['widget'] = Textarea(attrs={'rows': '3', 'cols': '120'})
        return super(Graph2FormAdmin, self).formfield_for_dbfield(db_field, **kwargs)

    duplicate_records.short_description = "Duplicate selected records"


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


admin.site.register(Graph2Query, Graph2QueryAdmin)


class Graph2GraphAdmin(admin.ModelAdmin):
    model = Graph2Graph
    search_fields = ('name', 'description')
    list_display = ('name', 'tags_list', 'description',
                    'form', 'page', 'query')
    fieldsets = ((None, {'fields': (('name', 'tags',))}),
                 ('Description', {
                     'classes': ('collapse',),
                     'fields': ('description',)}),
                 ('Form', {
                     'classes': ('collapse',),
                     'fields': ('form',)}),
                 ('Page', {
                     'classes': ('collapse',),
                     'fields': ('page',)}),
                 ('Query', {
                     'classes': ('collapse',),
                     'fields': ('query',)}),
    )
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
        return HttpResponseRedirect("/graphpages/graph/%s" % (selected[0]))

    graph_admin_action.short_description = 'Display graph'

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def duplicate_records(self, request, queryset):
        for obj in queryset:
            obj.id = None
            obj.name += '_dup'
            obj.save()

    duplicate_records.short_description = "Duplicate selected records"


admin.site.register(Graph2Graph, Graph2GraphAdmin)
