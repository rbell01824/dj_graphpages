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
# noinspection PyUnresolvedReferences
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import GraphPageTags, GraphPageGraph
from test_data.models import Countries, CIA
from django.views.generic.list import ListView
from django.views.generic import View, FormView


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
        gpg = get_object_or_404(GraphPageGraph, pk=graph_pk)
        if gpg.form or (gpg.form and gpg.form_ref.form):        # process form if present
            if gpg.form_ref:
                t = Template(gpg.form_ref.form)
            else:
                t = Template(gpg.form)
            c = Context({'graph_pk': gpg.pk})
            return HttpResponse(t.render(c))
        else:                               # no form, build and display the graph
            graph_graph_response = self.build_graph_graph_response(request, gpg)
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
        GraphPageobj = GraphPageGraph.objects.get(graph_pk)
        form = self.build_graph_form_class(GraphPageobj)
        # # ContactForm was defined in the the previous section
        # form = ContactForm(request.POST) # A form bound to the POST data
        # if form.is_valid(): # All validation rules pass
        #     # Process the data in form.cleaned_data
        #     # ...
        #     return HttpResponseRedirect('/thanks/') # Redirect after POST
        return HttpResponse('hi from GraphPageview post')

    # noinspection PyMethodMayBeStatic
    def build_graph_form_response(self, request, GraphPageobj):
        """
        Here we build a form from the graph form and return it.
        Subsequently, a post will return the form.
        """
        formclass = self.build_graph_form_class(GraphPageobj)      # create the form class
        form = formclass()                                      # create the unbound form
        template = Template(GraphPageobj.form)                     # create template object
        context = RequestContext(request, {'graph_pk': GraphPageobj.pk, 'form': form})
        response = template.render(context)
        return response

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def build_graph_form_class(self, GraphPageobj):
        """
        Create a form object from the form definition in a GraphPageobj.
        """
        match = re.match(r'.*{% form\s*[A-Za-z_0-9]*\s*%}(?P<THEFORM>.*){% endform\s*[A-Za-z_0-9]*\s*%}.*',
                         GraphPageobj.form, re.MULTILINE | re.DOTALL)
        if not match:
            raise ValidationError('Can not find form definition.')
        form_text = match.group('THEFORM')
        exec(form_text, globals(), locals())
        # noinspection PyUnresolvedReferences
        return GraphForm            # return the graphform class

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def build_graph_graph_response(self, request, GraphPageobj):
        """
        If there is a query, get it and exec.
        Otherwise just display the page.

        :param request:
        :type request:
        :param GraphPageobj:
        :type GraphPageobj: GraphPageGraph
        """
        context = self.execute_query_to_build_context(request, GraphPageobj)
        template = self.get_graph_template(GraphPageobj)
        response = template.render(context)
        return response

    # noinspection PyMethodMayBeStatic
    def execute_query_to_build_context(self, request, GraphPageobj):
        """
        :param GraphPageobj:
        :type GraphPageobj: Graph2Graph
        """
        # todo 2: make exec safe
        # todo 2: rewrite to use globals and locals properly
        # todo 1: if there is a request post context then we need to get that data into local() context
        if not GraphPageobj.query:
            return Context({})
        query_text = GraphPageobj.query
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
    def get_graph_template(self, GraphPageobj):
        """
        :param GraphPageobj:
        :type GraphPageobj: Graph2Graph
        """
        template_text = ''
        if GraphPageobj.template:                      # use page if available
            template_text = GraphPageobj.template
        # todo 2: other validations go here
        return Template(template_text)


###############################################################################


class GraphPageGraphListView(ListView):
    model = GraphPageGraph
