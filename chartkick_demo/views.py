#!/usr/bin/env python

"""

11/18/13 - Initial creation

Dependencies:
pip install django

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

from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the demo index.")


def charts(request):
    exchange = {'2001-01-31': 1.064, '2002-01-31': 1.1305,
                '2003-01-31': 0.9417, '2004-01-31': 0.7937,
                '2005-01-31': 0.7609, '2006-01-31': 0.827,
                '2007-01-31': 0.7692, '2008-01-31': 0.6801,
                '2009-01-31': 0.7491, '2010-01-31': 0.7002,
                '2011-01-31': 0.7489, '2012-01-31': 0.7755,
                '2013-01-31': 0.7531,
                }

    browser_stats = [['Chrome', 52.9], ['Firefox', 27.7], ['Opera', 1.6],
                     ['Internet Explorer', 12.6], ['Safari', 4]]

    temperature = [{u'data': {'2012-00-01 00:00:00 -0700': 7,
                              '2012-01-01 00:00:00 -0700': 6.9,
                              '2012-02-01 00:00:00 -0700': 9.5,
                              '2012-03-01 00:00:00 -0700': 14.5,
                              '2012-04-01 00:00:00 -0700': 18.2,
                              '2012-05-01 00:00:00 -0700': 21.5,
                              '2012-06-01 00:00:00 -0700': 25.2,
                              '2012-07-01 00:00:00 -0700': 26.5,
                              '2012-08-01 00:00:00 -0700': 23.3,
                              '2012-09-01 00:00:00 -0700': 18.3,
                              '2012-10-01 00:00:00 -0700': 13.9,
                              '2012-11-01 00:00:00 -0700': 9.6},
                    u'name': u'Tokyo'},
                   {u'data': {'2012-00-01 00:00:00 -0700': -0.2,
                              '2012-01-01 00:00:00 -0700': 0.8,
                              '2012-02-01 00:00:00 -0700': 5.7,
                              '2012-03-01 00:00:00 -0700': 11.3,
                              '2012-04-01 00:00:00 -0700': 17,
                              '2012-05-01 00:00:00 -0700': 22,
                              '2012-06-01 00:00:00 -0700': 24.8,
                              '2012-07-01 00:00:00 -0700': 24.1,
                              '2012-08-01 00:00:00 -0700': 20.1,
                              '2012-09-01 00:00:00 -0700': 14.1,
                              '2012-10-01 00:00:00 -0700': 8.6,
                              '2012-11-01 00:00:00 -0700': 2.5},
                    u'name': u'New York'},
                   {u'data': {'2012-00-01 00:00:00 -0700': -0.9,
                              '2012-01-01 00:00:00 -0700': 0.6,
                              '2012-02-01 00:00:00 -0700': 3.5,
                              '2012-03-01 00:00:00 -0700': 8.4,
                              '2012-04-01 00:00:00 -0700': 13.5,
                              '2012-05-01 00:00:00 -0700': 17,
                              '2012-06-01 00:00:00 -0700': 18.6,
                              '2012-07-01 00:00:00 -0700': 17.9,
                              '2012-08-01 00:00:00 -0700': 14.3,
                              '2012-09-01 00:00:00 -0700': 9,
                              '2012-10-01 00:00:00 -0700': 3.9,
                              '2012-11-01 00:00:00 -0700': 1},
                    u'name': u'Berlin'},
                   {u'data': {'2012-00-01 00:00:00 -0700': 3.9,
                              '2012-01-01 00:00:00 -0700': 4.2,
                              '2012-02-01 00:00:00 -0700': 5.7,
                              '2012-03-01 00:00:00 -0700': 8.5,
                              '2012-04-01 00:00:00 -0700': 11.9,
                              '2012-05-01 00:00:00 -0700': 15.2,
                              '2012-06-01 00:00:00 -0700': 17,
                              '2012-07-01 00:00:00 -0700': 16.6,
                              '2012-08-01 00:00:00 -0700': 14.2,
                              '2012-09-01 00:00:00 -0700': 10.3,
                              '2012-10-01 00:00:00 -0700': 6.6,
                              '2012-11-01 00:00:00 -0700': 4.8},
                    u'name': u'London'}]

    sizes = [['X-Small', 5], ['Small', 27], ['Medium', 10],
             ['Large', 14], ['X-Large', 10]]

    areas = {'2013-07-27 07:08:00 UTC': 4, '2013-07-27 07:09:00 UTC': 3,
             '2013-07-27 07:10:00 UTC': 2, '2013-07-27 07:04:00 UTC': 2,
             '2013-07-27 07:02:00 UTC': 3, '2013-07-27 07:00:00 UTC': 2,
             '2013-07-27 07:06:00 UTC': 1, '2013-07-27 07:01:00 UTC': 5,
             '2013-07-27 07:05:00 UTC': 5, '2013-07-27 07:03:00 UTC': 3,
             '2013-07-27 07:07:00 UTC': 3}

    return render(request, 'chartkick_demo.html', locals())
