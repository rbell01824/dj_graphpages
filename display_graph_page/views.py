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

from django.shortcuts import render
from django.http import HttpResponse

from graphpages.models import GraphPage


def list_graphs(request, query):
    if query == '_':                                # if no query just show them all
        qs = GraphPage.objects.order_by('name')
    else:                                           # otherwise show the query results
        # todo 1: work out query details
        qs = GraphPage.objects.order_by('name')
    # rsp = 'Hi the query is <<{}>>'.format(query)
    # return HttpResponse(rsp)
    return render(request, 'list_graphs.html', qs)
