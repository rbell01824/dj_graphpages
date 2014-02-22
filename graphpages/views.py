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
from django.template import Context, Template

from .models import GraphTemplates, GraphTemplateTags
from .models import GraphPage, GraphPageTags
from test_data.models import Countries, CIA
from django.views.generic.list import ListView


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
    # todo 1: rewrite to use globals and locals properly
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


class GraphListView(ListView):
    model = GraphPage
