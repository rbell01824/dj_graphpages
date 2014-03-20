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
# from django.utils.text import slugify
from django.forms import Textarea, TextInput
from django.contrib import admin

# from .models import GraphPageTags, GraphPage
from .models import GraphPageGraph, GraphPageTags

from django.utils.translation import ugettext_lazy as _
from django.contrib.admin import SimpleListFilter

from taggit.models import TaggedItem
from taggit_suggest.utils import suggest_tags


class TaggitListFilter(SimpleListFilter):
    """
    A custom filter class that can be used to filter by taggit tags in the admin.

    code from https://djangosnippets.org/snippets/2807/
    """

    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('tags')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'tag'

    # noinspection PyUnusedLocal,PyShadowingBuiltins
    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each tuple is the coded value
        for the option that will appear in the URL query. The second element is the
        human-readable name for the option that will appear in the right sidebar.
        """
        list = []
        tags = TaggedItem.tags_for(model_admin.model)
        for tag in tags:
            list.append((tag.name, _(tag.name)), )
        return list

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value provided in the query
        string and retrievable via `self.value()`.
        """
        if self.value():
            return queryset.filter(tags__name__in=[self.value()])


class GraphPageTagsAdmin(admin.ModelAdmin):
    model = GraphPageTags
    search_fields = ('tag', 'description')
    list_display = ('tag', 'description',)
    fields = ('tag', 'description')
    # list_editable = ('description',)
    save_on_top = True
    pass
admin.site.register(GraphPageTags, GraphPageTagsAdmin)


class GraphPageGraphAdmin(admin.ModelAdmin):

    # noinspection PyMethodMayBeStatic
    def display_graph(self, obj):
        rtn = u"<div><a class='btn btn-primary btn-sm' href='/graphpages/graphpage/%s'>Display</a></div>" % obj.id
        return rtn
    display_graph.short_description = ''
    display_graph.allow_tags = True

    # noinspection PyMethodMayBeStatic
    def tags_suggest(self, obj):
        """
        Suggest tags based on description
        """
        return suggest_tags(content=obj.description)

    model = GraphPageGraph
    search_fields = ('name', 'description')
    readonly_fields = ('form_slug', 'query_slug', 'template_slug', 'tags_suggest')
    list_display = ('display_graph', 'name', 'tags_slug', 'description',
                    'form_slug', 'query_slug', 'template_slug'
                    )
    fieldsets = (
        (None, {'classes': ('suit-tab suit-tab-general',),
                'fields': ('name', 'description', ('tags', 'tags_suggest'))}),
        ('Form', {'classes': ('suit-tab suit-tab-form',),
                  'fields': ('form_ref', 'form',)}),
        ('Form Page', {'classes': ('suit-tab suit-tab-formpage',),
                       'fields': ('form_page_ref', 'form_page',)}),
        ('Query', {'classes': ('suit-tab suit-tab-query',),
                   'fields': ('query_ref', 'query',)}),
        ('Graph Page', {'classes': ('suit-tab suit-tab-graphpage',),
                        'fields': ('template_ref', 'template',)}),
    )
    list_display_links = ('name',)
    list_filter = (TaggitListFilter,)
    suit_form_tabs = (('general', 'General'),
                      ('form', 'Form'),
                      ('formpage', 'Form Page'),
                      ('query', 'Query'),
                      ('graphpage', 'Graph Page')
                      )
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
        for tag in obj.tags.names():
            rtn += '; ' + tag
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
            kwargs['widget'] = Textarea(attrs={'class': 'span12', 'rows': '30', 'cols': '140'})
        if db_field.name == 'form_page':
            kwargs['widget'] = Textarea(attrs={'class': 'span12', 'rows': '30', 'cols': '140'})
        if db_field.name == 'query':
            kwargs['widget'] = Textarea(attrs={'class': 'span12', 'rows': '30', 'cols': '140'})
        if db_field.name == 'template':
            kwargs['widget'] = Textarea(attrs={'class': 'span12', 'rows': '30', 'cols': '140'})
        return super(GraphPageGraphAdmin, self).formfield_for_dbfield(db_field, **kwargs)

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
            newobj.tags.add(*obj.my_tags.all())
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
admin.site.register(GraphPageGraph, GraphPageGraphAdmin)
