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


from django.views.generic import View
from django.views.generic import ListView
from django.http import HttpResponse

from graphpages.utilities import xgraph_response

from .models import CIA, Countries
from .democharts import syslog_demo_8b


# noinspection PyDocstring
class ListCIAView(ListView):
    model = CIA


# noinspection PyDocstring
class ListCountriesView(ListView):
    model = Countries


class Demo8bView(View):
    """
    View class to test demo8b method.
    """

    # noinspection PyMethodMayBeStatic
    def get(self, request):
        """
        Executre the graph method and display the results.

        :param request:
        """
        context = syslog_demo_8b()
        return HttpResponse(xgraph_response(context))
