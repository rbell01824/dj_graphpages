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
    model = CIA
    search_fields = ('name', 'country_code')
    # list_filter = ('is_active', 'users', 'created_by', 'created_on', 'status')
    # ordering = ('name')
    list_display = ('name', 'country_code', 'total_area', 'coastline',
                    'population', 'birth_rate', 'p_growth',
                    'phone_mobiles', 'internet_users')
    fields = (('name', 'country_code'),
              ('total_area', 'land_area', 'water_area'),
              ('coastline', 'total_border'),
              ('labor_force', 'p_young', 'p_adult', 'p_old', 'p_growth'),
              ('phone_mobiles', 'phone_mainlines'),
              ('internet_users', 'isps'),
              ('birth_rate', 'death_rate'))
    # filter_horizontal = ('users',)
    save_on_top = True
    pass
admin.site.register(CIA, CIAAdmin)


class CountriesAdmin(admin.ModelAdmin):
    pass
admin.site.register(Countries, CountriesAdmin)
