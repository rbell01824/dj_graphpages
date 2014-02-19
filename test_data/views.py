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

import csv
import os
import sys

from django.shortcuts import render
from django.http import HttpResponse

# from .models import BabyNames
#
#
# def import_names():
#     BabyNames.objects.all().delete()
#     with open('graphtestdata/data-baby-names-master/baby-names.csv') as f:
#         reader = csv.reader(f)
#         fc = True
#         cnt = 0
#         for row in reader:
#             if fc:
#                 print row
#                 fc = False
#                 continue
#             cnt += 1
#             if cnt % 10 == 0:
#                 sys.stdout.write('.')
#             if cnt % 100 == 0:
#                 sys.stdout.write(' ')
#             if cnt % 1000 == 0:
#                 print
#             bn, created = BabyNames.objects.get_or_create(year=row[0],
#                                                           name=row[1],
#                                                           percent=row[2],
#                                                           sex=row[3])
#             bn.save()
#     pass
#
#
# def import_names_by_state():
#     pass
#
#
# def import_births():
#     pass
#
#
# def import_baby_names(request):
#     import_names()
#     import_names_by_state()
#     import_births()
#     return HttpResponse('hi dude')

