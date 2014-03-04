#!/usr/bin/env python
# coding=utf-8

""" Some description here

2/19/14 - Initial creation

"""

from __future__ import unicode_literals
import logging

log = logging.getLogger(__name__)

__author__ = 'richabel'
__date__ = '2/19/14'
__license__ = "All rights reserved"
__version__ = "0.1"
__status__ = "dev"

import re

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.db.models import Sum
from django.template import Context, RequestContext, Template
from django import forms

from .models import GraphTemplates, GraphTemplateTags
from .models import GraphPage, GraphPageTags, Graph2Graph, Graph3Graph
from test_data.models import Countries, CIA
from django.views.generic.list import ListView
from django.views.generic import View


def get_graph_template(graphpage_obj):
    template_text = ''
    if graphpage_obj.template:          # use template if available
        template_text = graphpage_obj.template.template
    elif graphpage_obj.page:            # use page if available
        template_text = graphpage_obj.page
    if len(template_text) == 0:     # no template
        raise ValidationError('Graph improperly configured. No template. No page.')
    # todo 2: other validations go here
    return Template(template_text)


# noinspection PyUnusedLocal
def get_query_text(graphpage_obj):
    query_text = ''
    if not graphpage_obj.query:
        raise ValidationError('Graph improperly configured. No query.')
    query_text = graphpage_obj.query
    # todo 2: other validations go here
    # query_text = query_text.strip('\r\n', '\n')
    return query_text


def get_context(graphpage_obj):
    # todo 2: make exec safe
    # todo 2: rewrite to use globals and locals properly
    exec(get_query_text(graphpage_obj), None, None)
    context = Context(locals())
    return context


def build_graph_response(graphpage_obj):
    template = get_graph_template(graphpage_obj)
    context = get_context(graphpage_obj)
    response = template.render(context)
    return response


def graph(request, graph_pk):
    # return HttpResponse('Hi dude')
    graphpage_obj = get_object_or_404(GraphPage, pk=graph_pk)
    response = build_graph_response(graphpage_obj)
    return HttpResponse(response)

###############################################################################


class Graph2View(View):

    # noinspection PyMethodMayBeStatic
    def get(self, request, graph_pk):
        """
        If there is a form, display it.  When the form is posted control will return to the post method.
        If no form, then display the graph
        """
        graph2obj = get_object_or_404(Graph2Graph, pk=graph_pk)
        if graph2obj.form:
            self.graph_form(request, graph2obj)
        # no form, so deal with the template and query
        response = self.build_graph_response(request, graph2obj)
        return HttpResponse(response)

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def post(self, request, graph_pk):
        """
        :param request:
        :type request:
        :param graph_pk:
        :type graph_pk:
        """
        return HttpResponse('hi from graph2view post')

    # noinspection PyMethodMayBeStatic
    def graph_form(self, request, graph2obj):
        """
        Here we build a form from the graph form and return it.  Subsequently, a post will return the form.
        """
        raise ValidationError('Graph improperly configured. No form.')

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def build_graph_response(self, request, graph2obj):
        """
        If there is a query, get it and exec.  Otherwise everything must be in the page.

        :param request:
        :type request:
        :param graph2obj:
        :type graph2obj: Graph2Graph
        """
        context = self.get_query_context(graph2obj)
        template = self.get_graph_template(graph2obj)
        response = template.render(context)
        return response

    # noinspection PyMethodMayBeStatic
    def get_query_context(self, graph2obj):
        """
        :param graph2obj:
        :type graph2obj: Graph2Graph
        """
        if not graph2obj.query:
            return Context({})
        query_text = graph2obj.query.query
        if len(query_text.strip()) <= 0:
            return Context({})
        # global_context = {}
        # local_context = {}
        query_text = query_text.strip()
        exec(query_text, None, None)
        context = Context(locals())
        return context

    # noinspection PyMethodMayBeStatic
    def get_graph_template(self, graph2obj):
        """
        :param graph2obj:
        :type graph2obj: Graph2Graph
        """
        template_text = ''
        if graph2obj.template:              # use page if available
            template_text = graph2obj.template.template
        return Template(template_text)

###############################################################################


class Graph3View(View):

    # noinspection PyMethodMayBeStatic
    def get(self, request, graph_pk):
        """
        If there is a form, display it.  When the form is posted control will return to the post method.
        There we will build and display the graph.

        If no form, then build and display the graph here.
        """
        graph3obj = get_object_or_404(Graph3Graph, pk=graph_pk)
        if graph3obj.form:                  # process form if present
            graph_form_response = self.build_graph_form_response(request, graph3obj)
            return HttpResponse(graph_form_response)
        else:                               # no form, build and display the graph
            graph_graph_response = self.build_graph_graph_response(request, graph3obj)
            return HttpResponse(graph_graph_response)

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def post(self, request, graph_pk):
        """
        There was a form.  Process it and if valid build and display the graph.
        :param request:
        :type request:
        :param graph_pk:
        :type graph_pk:
        """
        graph3obj = Graph3Graph.objects.get(graph_pk)
        form = self.build_graph_form(graph3obj)
        # todo 1: view logic
        # # ContactForm was defined in the the previous section
        # form = ContactForm(request.POST) # A form bound to the POST data
        # if form.is_valid(): # All validation rules pass
        #     # Process the data in form.cleaned_data
        #     # ...
        #     return HttpResponseRedirect('/thanks/') # Redirect after POST
        return HttpResponse('hi from graph3view post')

    # noinspection PyMethodMayBeStatic
    def build_graph_form_response(self, request, graph3obj):
        """
        Here we build a form from the graph form and return it.
        Subsequently, a post will return the form.
        """
        form = self.build_graph_form(graph3obj)     # create the unbound form
        template = Template(graph3obj.form)         # create template object
        context = RequestContext(request, {'graph_pk': graph3obj.pk, 'form': form})
        response = template.render(context)
        return response

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def build_graph_form(self, graph3obj):
        """
        Create a form object from the form definition in a graph3obj.
        """
        match = re.match(r'.*{% form\s*[A-Za-z_0-9]*\s*%}(?P<THEFORM>.*){% endform\s*[A-Za-z_0-9]*\s*%}.*',
                         graph3obj.form, re.MULTILINE | re.DOTALL)
        if not match:
            raise ValidationError('Can not find form definition.')
        form_text = match.group('THEFORM')
        # todo 2: figure out why locals() has to be where globals should be and only pass in what is really needed
        exec(form_text, locals(), locals())
        # noinspection PyUnresolvedReferences
        form = GraphForm()                  # create the unbound form
        return form  this is an instance of an unbound form, what is really needed is the class

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def build_graph_graph_response(self, request, graph3obj):
        """
        If there is a query, get it and exec.
        Otherwise just display the page.

        :param request:
        :type request:
        :param graph3obj:
        :type graph3obj: Graph3Graph
        """
        context = self.execute_query_to_build_context(request, graph3obj)
        template = self.get_graph_template(graph3obj)
        response = template.render(context)
        return response

    # noinspection PyMethodMayBeStatic
    def execute_query_to_build_context(self, request, graph3obj):
        """
        :param graph3obj:
        :type graph3obj: Graph2Graph
        """
        # todo 2: make exec safe
        # todo 2: rewrite to use globals and locals properly
        # todo 1: if there is a request post context then we need to get that data into local() context
        if not graph3obj.query:
            return Context({})
        query_text = graph3obj.query
        if len(query_text.strip()) <= 0:
            return Context({})
        # global_context = {}
        # local_context = {}
        query_text = query_text.strip()
        # todo: run the query_text through Template to expand macros
        # todo: look into specifing locals and globals
        exec(query_text, None, None)
        context = Context(locals())
        return context

    # noinspection PyMethodMayBeStatic
    def get_graph_template(self, graph3obj):
        """
        :param graph3obj:
        :type graph3obj: Graph2Graph
        """
        template_text = ''
        if graph3obj.template:                      # use page if available
            template_text = graph3obj.template
        # todo 2: other validations go here
        return Template(template_text)

###############################################################################


class Graph3GraphListView(ListView):
    model = Graph3Graph
