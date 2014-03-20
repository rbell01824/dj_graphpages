#!/usr/bin/env python
# coding=utf-8

""" Some description here

3/9/14 - Initial creation

"""

from __future__ import unicode_literals
import logging

log = logging.getLogger(__name__)

__author__ = 'richabel'
__date__ = '3/9/14'
__license__ = "All rights reserved"
__version__ = "0.1"
__status__ = "dev"


from django.views.generic import FormView
from django.forms.extras.widgets import SelectDateWidget
from django import forms


class GraphFormX2(forms.Form):
    title = forms.CharField(min_length=3, max_length=80, label='Title')
    number_countries = forms.IntegerField(max_value=50, min_value=5,
                                          label='Number of countries')


class GraphFormX2View(FormView):
    template_name = 'graphformx2.html'
    form_class = GraphFormX2
