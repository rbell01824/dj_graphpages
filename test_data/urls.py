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

from django.conf.urls import patterns, include, url

from test_data.views import ListCIAView
from test_data.views import ListCountriesView
from test_data.views import Demo8bView

urlpatterns = patterns('',
                       url(r'demo8b$', Demo8bView.as_view(), name='demo8b'),
                       url(r'^cia$', ListCIAView.as_view(), name='cia_list', ),
                       url(r'^countries$', ListCountriesView.as_view(), name='countries_list', ),
                       )
