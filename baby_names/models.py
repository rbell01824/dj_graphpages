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


class BabyNames(models.Model):
    """
    Basic baby names table
    """
    year = models.IntegerField()
    name = models.CharField(max_length=30)
    percent = models.FloatField()
    sex = models.CharField(max_length=5)

    class Meta:
        verbose_name = 'Baby Name'
        verbose_name_plural = 'Baby Names'

    def __unicode__(self):
        return u'{}.{}.{}.{}'.format(self.year, self.name, self.percent, self.sex)


class BabyNamesByState(models.Model):
    """
    Baby names by state
    """
    state = models.CharField(max_length=2)
    year = models.IntegerField()
    name = models.CharField(max_length=30)
    number = models.IntegerField()
    sex = models.CharField(max_length=5)

    class Meta:
        verbose_name = 'Baby Names By State'
        verbose_name_plural = 'Baby Names By States'

    def __unicode__(self):
        return u'{}.{}.{}.{}.{}'.format(self.state, self.year, self.name, self.number, self.sex)


class Births(models.Model):
    """
    Baby births
    """
    year = models.IntegerField()
    state = models.CharField(max_length=2)
    sex = models.CharField(max_length=5)
    births = models.IntegerField()

    class Meta:
        verbose_name = 'Births'
        verbose_name_plural = 'Births'

    def __unicode__(self):
        return u'{}.{}.{}.{}'.format(self.year, self.state, self.sex, self.births)
