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
from django.views.generic.list import ListView
from django.views.generic import View, FormView

# Supress unresolvedreferences as these are actually needed inside
# the form exec.
# noinspection PyUnresolvedReferences
from django import forms

from .models import GraphPage

# Supress unresolvedreferences as these are actually needed inside
# the exec for the graph query.
# noinspection PyUnresolvedReferences
from test_data.models import Countries, CIA

from django.conf import settings

# todo 1: install and user python-markdown2 from https://github.com/trentm/python-markdown2


class GraphPageView(View):
    """
    View class for graph pages
    """

    # noinspection PyMethodMayBeStatic
    def get(self, request, graph_pk):
        """
        If there is a form, display it.  When the form is posted control will return to the post method.
        There we will build and display the graph.

        If no form, then build and display the graph here.
        :param request:
        :param graph_pk: Primary key for graphpage
        """
        # todo 1: modify graphpage to use graph slug instead of PK
        gpg = get_object_or_404(GraphPage, pk=graph_pk)
        if gpg.form or (gpg.form and gpg.form_ref.form):        # process form if present
            return HttpResponse(self.display_form(request, gpg))
        else:                                                   # no form, build and display the graph
            return HttpResponse(self.build_graph_graph_response(request, gpg))

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def post(self, request, graph_pk):
        """
        There was a form.  Process it and if valid build and display the graph.
        :param request:
        :param graph_pk: Primary key for graphpage
        """
        gpg = GraphPage.objects.get(pk=graph_pk)
        form_class_obj, context = self.get_form_object_and_context(gpg)
        form = form_class_obj(request.POST)
        if form.is_valid():
            return HttpResponse(self.build_graph_graph_response(request, gpg, request.POST))
        # form not valid, so redisplay form with errors
        form_page = self.get_form_page(gpg)
        t = Template(form_page)
        c = RequestContext(request, {'graph_pk': str(gpg.pk), 'graphform': form})
        return HttpResponse(t.render(c))

    def display_form(self, request, gpg):
        """
        Display the graphpage form page.
        :param request:
        :param gpg: graphpage object
        """
        # get the form and form_page
        form_class_obj, context = self.get_form_object_and_context(gpg)
        form_page = self.get_form_page(gpg)
        # create unbound form object
        graphform = form_class_obj()
        # render response
        t = Template(form_page)
        c = RequestContext(request, {'graph_pk': str(gpg.pk), 'graphform': graphform})
        return t.render(c)

    # noinspection PyUnresolvedReferences,PyMethodMayBeStatic
    def get_form_object_and_context(self, gpg):
        """
        Get the forms.form object
        :param gpg: graphpage object
        """
        # get the form definition
        if gpg.form_ref:
            form = gpg.form_ref.form.strip()
        else:
            form = gpg.form.strip()
        if len(form) == 0:
            raise ValidationError('Empty form')
        # deal with any markup
        # todo 1: here deal with markup in form
        # create the form object
        exec(form, globals(), locals())
        return GraphForm, locals()

    # noinspection PyMethodMayBeStatic
    def get_form_page(self, gpg):
        """
        Get the form page
        :param gpg: graphpage object
        """
        # get the form page definition
        if gpg.form_page_ref:
            page = gpg.form_page_ref.form.strip()
        else:
            page = gpg.form_page.strip()
        if len(page) == 0:
            raise ValidationError('Empty form page')
        # deal with any markup
        # todo 1: here deal with markup in form
        conf = settings.GRAPHPAGE_CONFIG
        return conf['formpageheader'] + page + conf['formpagefooter']

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def build_graph_graph_response(self, request, gpg, form_context=None):
        """
        If there is a query, get it and exec.
        Otherwise just display the page.

        :type request: WSGIRequest
        :type gpg: GraphPage oject
        :type form_context: QueryDict, If there was a form the request.POST value
        """
        context = self.execute_query_to_build_context(request, gpg, form_context)
        template = self.get_graph_page_template(gpg)
        response = template.render(context)
        return response

    # noinspection PyMethodMayBeStatic
    def execute_query_to_build_context(self, request, gpg, form_context=None):
        """
        Execute a grasph form query.  This creates a context that is used by the graph page
        to actually display the form.
        :type request: WSGIRequest
        :type gpg: GraphPage object
        :type form_context: dict, if there was a form the POST dictionary
        """
        if not form_context:
            form_context = {}
        # todo 2: make exec safe
        # See if there is a query
        if not gpg.query:
            return Context({})
        query_text = gpg.query.strip()
        if len(query_text) <= 0:
            return Context({})
        # There is so we'll need to exec it.
        # See if there is a form _context.  If there is, get it into our local context.
        fc = {}
        if form_context:
            fc = form_context.dict()
        # deal with any markup
        # todo 1: here deal with markup in query
        # There may be some template tags in the query so process them.
        t = Template(query_text)
        c = Context(fc)
        query_text = t.render(c)

        exec(query_text, None, locals())
        fc.update(locals())
        context = Context(fc)
        return context

    # noinspection PyMethodMayBeStatic
    def get_graph_page_template(self, gpg):
        """
        :type gpg: graphpage object
        """
        graph_page_text = ''
        if gpg.graph_page:                      # use page if available
            graph_page_text = gpg.graph_page
        # deal with any markup
        # todo 1: here deal with markup in graph themplate
        # todo 2: other validations go here
        conf = settings.GRAPHPAGE_CONFIG
        graph_page_text = conf['graphpageheader'] + graph_page_text + conf['graphpagefooter']
        return Template(graph_page_text)


###############################################################################


class GraphPageListView(ListView):
    """
    ListView for graphpages
    """
    model = GraphPage

    def get_queryset(self):
        """
        Force queryset sort order.
        """
        return GraphPage.objects.all().order_by('title')
