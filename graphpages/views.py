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

from .models import GraphTemplates, GraphTemplateTags
from .models import GraphPage, GraphPageTags, Graph2Graph, Graph3Graph
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
            # graph_form_response = self.build_graph_form_response(request, graph3obj)
            t = Template(graph3obj.form)
            c = Context({'graph_pk': graph3obj.pk})
            return HttpResponse(t.render(c))
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
        form = self.build_graph_form_class(graph3obj)
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
        formclass = self.build_graph_form_class(graph3obj)      # create the form class
        form = formclass()                                      # create the unbound form
        template = Template(graph3obj.form)                     # create template object
        context = RequestContext(request, {'graph_pk': graph3obj.pk, 'form': form})
        response = template.render(context)
        return response

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def build_graph_form_class(self, graph3obj):
        """
        Create a form object from the form definition in a graph3obj.
        """
        match = re.match(r'.*{% form\s*[A-Za-z_0-9]*\s*%}(?P<THEFORM>.*){% endform\s*[A-Za-z_0-9]*\s*%}.*',
                         graph3obj.form, re.MULTILINE | re.DOTALL)
        if not match:
            raise ValidationError('Can not find form definition.')
        form_text = match.group('THEFORM')
        exec(form_text, globals(), locals())
        # noinspection PyUnresolvedReferences
        return GraphForm            # return the graphform class

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


###############################################################################


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
#
# Test crispy forms to make sure it's working
#
from crispy_forms.helper import FormHelper
# noinspection PyUnresolvedReferences
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions


class SimpleForm(forms.Form):
    text_input = forms.CharField()

    textarea = forms.CharField(
        widget=forms.Textarea(),
    )

    radio_buttons = forms.ChoiceField(
        choices=(
            ('option_one', "Option one is this and that be sure to include why it's great"),
            ('option_two', "Option two can is something else and selecting it will deselect option one")
        ),
        widget = forms.RadioSelect,
        initial = 'option_two',
    )

    checkboxes = forms.MultipleChoiceField(
        choices=(
            ('option_one', "Option one is this and that be sure to include why it's great"),
            ('option_two', 'Option two can also be checked and included in form results'),
            ('option_three', 'Option three can yes, you guessed it also be checked and included in form results')
        ),
        initial = 'option_one',
        widget = forms.CheckboxSelectMultiple,
        help_text = "<strong>Note:</strong> "
                    "Labels surround all the options for much larger click areas and a more usable form.",
    )

    appended_text = forms.CharField(
        help_text="Here's more help text"
    )

    prepended_text = forms.CharField()

    prepended_text_two = forms.CharField()

    multicolon_select = forms.MultipleChoiceField(
        choices=(('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')),
    )

    # Uni-form
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.layout = Layout(
        Field('text_input', css_class='input-xlarge'),
        Field('textarea', rows="3", css_class='input-xlarge'),
        'radio_buttons',
        Field('checkboxes', style="background: #FAFAFA; padding: 10px;"),
        AppendedText('appended_text', '.00'),
        PrependedText('prepended_text',
                      '<input type="checkbox" checked="checked" value="" id="" name="">', active=True),
        PrependedText('prepended_text_two', '@'),
        'multicolon_select',
        FormActions(
            Submit('save_changes', 'Save changes', css_class="btn-primary"),
            Submit('cancel', 'Cancel'),
        )
    )


class CrispyView(FormView):
    template_name = 'crispy.html'
    form_class = SimpleForm

# noinspection PyStatementEffect
"""
{% extends "base.html" %}
{% load graphpage %}
{% load crispy_forms_tags %}

{% block content %}
    <div class="container-fluid">
        <div class="row">
            <div class="col-md-6">
                <h3>This is a form page</h3>
                <p>It contains one or more forms, like the one below.</p>
                <p>You can put any explanation text above the form.</p>
            </div>
        </div>

{% form no_countries %}
class GraphForm(forms.Form):
    title = forms.CharField(min_length=3, max_length=80, label='Title')
    number_countries = forms.IntegerField(max_value=50, min_value=5,
                                          label='Number of countries')
    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_action = 'graphpages/graphpage3/{{graph_pk}}'
    helper.add_input(Submit('submit', 'Show graph', css_class='btn-primary'))
{% endform no_countries %}

        <div class="row">
            <div class="col-md-6">
               </br>
               <p>Likewise you can put any instructions or whatever after the form.</p>
               <p>Forms support django-crispy-forms and bootstrap3!</p>
            </div>
        </div>
    </div>
{% endblock content %}
"""

# noinspection PyStatementEffect
"""
{% extends "base.html" %}
{% load chartkick %}

{% query %}
title1 = 'Top {{number_countries}} countries by land area'
r = CIA.objects.order_by('-land_area')[:{{number_countries}}]
data1 = [[o.name, o.land_area] for o in r]

title2 = 'Top {{number_countries}} countries by population'
r = CIA.objects.order_by('-population')[:{{number_countries}}]
data2 = [[o.name, o.population] for o in r]
{% endquery %}

{% block content %}
    <div class="container-fluid">
        <div class="jumbotron">
            <h3>Django Graph Pages</h3>
            <p>This template displays two pie charts side by side in a fluid grid.</p>
        </div>
    </div>

    <div class="container-fluid">
        <div class="row">
            <div class="col-md-6">
                <h3>{{ title1 }}</h3>
                {% pie_chart data1 with id='chart-1' %}
                <a class="btn btn-primary" href="javascript:history.back()">Back</a>

            </div>
            <div class="col-md-6">
                <h3>{{ title2 }}</h3>
                {% pie_chart data2 with id='chart-2' %}
                <a class="btn btn-primary" href="javascript:history.back()">Back</a>
            </div>
        </div>
    </div>
{% endblock content %}
"""
