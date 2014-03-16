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
# noinspection PyUnresolvedReferences
from crispy_forms.helper import FormHelper
# noinspection PyUnresolvedReferences
from crispy_forms.layout import Submit, Layout, Field
# noinspection PyUnresolvedReferences
from crispy_forms.bootstrap import (PrependedAppendedText,
                                    PrependedText,
                                    FormActions)

from .models import GraphPageTags, GraphPageGraph
from test_data.models import Countries, CIA

from django.conf import settings


class GraphForm(forms.Form):
    title = forms.CharField(min_length=3, max_length=80, label='Title')
    number_countries = forms.IntegerField(max_value=50, min_value=5,
                                          label='Number of countries')
    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Show graph', css_class='btn-primary'))


###############################################################################


class GraphPageView(View):

    # noinspection PyMethodMayBeStatic
    def get(self, request, graph_pk):
        """
        If there is a form, display it.  When the form is posted control will return to the post method.
        There we will build and display the graph.

        If no form, then build and display the graph here.
        """
        # todo 1: modify graphpage to use graph slug instead of PK
        gpg = get_object_or_404(GraphPageGraph, pk=graph_pk)
        if gpg.form or (gpg.form and gpg.form_ref.form):        # process form if present
            return HttpResponse(self.display_form(request, gpg))
        else:                                                   # no form, build and display the graph
            return HttpResponse(self.build_graph_graph_response(request, gpg))

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def post(self, request, graph_pk):
        """
        There was a form.  Process it and if valid build and display the graph.
        :param request:
        :type request:
        :param graph_pk:
        :type graph_pk:
        """
        gpg = GraphPageGraph.objects.get(pk=graph_pk)
        form_class_obj, context = self.get_form_object(gpg)
        form = form_class_obj(request.POST)
        if form.is_valid():
            return HttpResponse(self.build_graph_graph_response(request, gpg, request.POST))
        # form not valid, so redisplay form with errors
        template = self.get_form_template(gpg)
        t = Template(template)
        c = RequestContext(request, {'graph_pk': str(gpg.pk), 'graphform': form})
        return HttpResponse(t.render(c))

    def display_form(self, request, gpg):
        """
        Display the graphpage form page.
        """
        # get the form and template
        form_class_obj, context = self.get_form_object(gpg)
        template = self.get_form_template(gpg)
        # create unbound form object
        graphform = form_class_obj()
        # render response
        t = Template(template)
        c = RequestContext(request, {'graph_pk': str(gpg.pk), 'graphform': graphform})
        return t.render(c)

    # noinspection PyUnresolvedReferences,PyMethodMayBeStatic
    def get_form_object(self, gpg):
        """
        Get the forms.form object
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
    def get_form_template(self, gpg):
        """
        Get the form template
        """
        # get the form template definition
        if gpg.form_page_ref:
            page = gpg.form_page_ref.form.strip()
        else:
            page = gpg.form_page.strip()
        if len(page) == 0:
            raise ValidationError('Empty form page')
        conf = settings.GRAPHPAGE_CONFIG
        return conf['formpageheader'] + page + conf['formpagefooter']

    # # noinspection PyMethodMayBeStatic
    # def build_graph_form_response(self, request, gpg_obj):
    #     """
    #     Here we build a form from the graph form and return it.
    #     Subsequently, a post will return the form.
    #     """
    #     formclass = self.build_graph_form_class(gpg_obj)      # create the form class
    #     form = formclass()                                      # create the unbound form
    #     template = Template(gpg_obj.form)                     # create template object
    #     context = RequestContext(request, {'graph_pk': gpg_obj.pk, 'form': form})
    #     response = template.render(context)
    #     return response
    #
    # # noinspection PyMethodMayBeStatic,PyUnusedLocal
    # def build_graph_form_class(self, gpg_obj):
    #     """
    #     Create a form object from the form definition in a GraphPageobj.
    #     """
    #     match = re.match(r'.*{% form\s*[A-Za-z_0-9]*\s*%}(?P<THEFORM>.*){% endform\s*[A-Za-z_0-9]*\s*%}.*',
    #                      gpg_obj.form, re.MULTILINE | re.DOTALL)
    #     if not match:
    #         raise ValidationError('Can not find form definition.')
    #     form_text = match.group('THEFORM')
    #     exec(form_text, globals(), locals())
    #     # noinspection PyUnresolvedReferences
    #     return GraphForm            # return the graphform class

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def build_graph_graph_response(self, request, gpg, form_context=None):
        """
        If there is a query, get it and exec.
        Otherwise just display the page.

        :param request:
        :type request: WSGIRequest
        :param gpg:
        :type gpg: GraphPageGraph
        :param form_context: If there was a form, the request.POST value
        :type form_context: QueryDict
        """
        context = self.execute_query_to_build_context(request, gpg, form_context)
        template = self.get_graph_template(gpg)
        response = template.render(context)
        return response

    # noinspection PyMethodMayBeStatic
    def execute_query_to_build_context(self, request, gpg, form_context=None):
        """
        :param gpg:
        :type gpg: Graph2Graph
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
        # There may be some template tags in the query so process them.
        t = Template(query_text)
        c = Context(fc)
        query_text = t.render(c)

        exec(query_text, None, locals())
        fc.update(locals())
        context = Context(fc)
        return context

    # noinspection PyMethodMayBeStatic
    def get_graph_template(self, gpg):
        """
        :param gpg:
        :type gpg: Graph2Graph
        """
        template_text = ''
        if gpg.template:                      # use page if available
            template_text = gpg.template
        # todo 2: other validations go here
        conf = settings.GRAPHPAGE_CONFIG
        template_text = conf['graphpageheader'] + template_text + conf['graphpagefooter']
        return Template(template_text)


###############################################################################


class GraphPageGraphListView(ListView):
    model = GraphPageGraph

