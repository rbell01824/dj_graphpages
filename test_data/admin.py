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


from django.contrib import admin
from .models import CIA, Countries


class CIAAdmin(admin.ModelAdmin):
    pass
admin.site.register(CIA, CIAAdmin)


class CountriesAdmin(admin.ModelAdmin):
    pass
admin.site.register(Countries, CountriesAdmin)
