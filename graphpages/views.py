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

from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template import Context, RequestContext, Template
from django.views.generic.list import ListView
from django.views.generic import View

# Supress unresolvedreferences as these are actually needed inside
# the form exec.
# noinspection PyUnresolvedReferences
from django import forms

from graphpages.models import GraphPage
from graphpages.utilities import XGraphPage, XGraphRow, XGraph

# Supress unresolvedreferences as these are actually needed inside
# the exec for the graph query.
# noinspection PyUnresolvedReferences
# from test_data.models import Countries, CIA
# todo 2: workout scheme to automagically import models that might be needed for query
# todo 2: django-extensions might be useful

# hack that may be a partial solution
# from django.db.models.loading import get_models
# for m in get_models():
#     exec "from %s import %s" % (m.__module__, m.__name__)

from django.conf import settings

# todo 3: install and use python-markdown2 from https://github.com/trentm/python-markdown2


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
        c = RequestContext(request, {'graph_pk': str(gpg.pk), 'graphform': graphform, 'form_context': context})
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
            page = '{% include "default_form_page.html" %}'
        return settings.GRAPHPAGE_FORMPAGEHEADER + page + settings.GRAPHPAGE_FORMPAGEFOOTER

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

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def execute_query_to_build_context(self, request, gpg, form_context=None):
        """
        Execute a grasph form query.  This creates a context that is used by the graph page
        to actually display the form.
        :type request: WSGIRequest
        :type gpg: GraphPage object
        :type form_context: dict, if there was a form the POST dictionary
        """
        global_context = dict(globals())
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
            # noinspection PyUnresolvedReferences
            fc = form_context.dict()
        # It it ever becomes necessary to support template tags the following code may be useful
        # There may be some template tags in the query so process them.
        # t = Template(query_text)
        # c = Context(fc)
        # query_text = t.render(c)

        exec(query_text, global_context, fc)
        context = Context(fc)
        return context

    # noinspection PyMethodMayBeStatic
    def get_graph_page_template(self, gpg):
        """
        :type gpg: graphpage object
        """
        # get the graph page definition
        if gpg.graph_page_ref:
            page = gpg.graph_page_ref.form.strip()
        else:
            page = gpg.graph_page.strip()
        if len(page) == 0:
            page = '{% include "default_graph_page.html" %}'
        conf = settings.GRAPHPAGE_CONFIG
        page = conf['graphpageheader'] + page + conf['graphpagefooter']
        return Template(page)


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
