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

from django.db import models


class CIA(models.Model):
    """
    ci world fact book
    """
    country_code = models.CharField(max_length=2, primary_key=True)
    name = models.CharField(max_length=50)
    total_area = models.FloatField()
    land_area = models.FloatField()
    water_area = models.FloatField()
    coastline = models.FloatField()
    total_border = models.FloatField()
    population = models.FloatField()
    p_young = models.FloatField()
    p_adult = models.FloatField()
    p_old = models.FloatField()
    p_growth = models.FloatField()
    labor_force = models.FloatField()
    phone_mobiles = models.FloatField()
    phone_mainlines = models.FloatField()
    internet_users = models.FloatField()
    isps = models.FloatField()
    birth_rate = models.FloatField()
    death_rate = models.FloatField()

    class Meta:
        verbose_name = 'CIA World Factbook'
        verbose_name_plural = 'CIA World Factbook'

    def __unicode__(self):
        return u'{}'.format(self.name)


class Countries(models.Model):
    """
    world countries
    """
    id = models.IntegerField(primary_key=True)
    a2 = models.CharField(max_length=2)
    a3 = models.CharField(max_length=2)
    num = models.IntegerField()
    country_name = models.CharField(max_length=50)
    country_size = models.IntegerField()
    population = models.IntegerField()
    life_expectancy = models.FloatField()
    infant_mortality = models.FloatField()

    class Meta:
        verbose_name = 'Countries'
        verbose_name_plural = 'Countries'

    def __unicode__(self):
        return u'{}'.format(self.country_name)
