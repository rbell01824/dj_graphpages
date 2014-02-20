#!/usr/bin/env python

"""

11/18/13 - Initial creation

Dependencies:


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


class GraphPageTags(models.Model):
    tag = models.CharField(max_length=20, unique=True, primary_key=True)
    description = models.TextField()

    class Meta:
        verbose_name = "Graph Page Tags"
        verbose_name_plural = "Graph Page Tags"

    def __unicode__(self):
        return u'{}'.format(self.tag)


class GraphPage(models.Model):
    """
    graph page
    """
    PAGE_FORMATS = (('html', 'html'),
                    ('rst', 'reStructuredText'),
                    ('md', 'markdown'))

    name = models.CharField(max_length=50, unique=True, primary_key=True)       # name of graph page
    description = models.TextField(blank=True)      # some sort of useful description
    tags = models.ManyToManyField(GraphPageTags,
                                  blank=True,
                                  null=True)
    form = models.TextField(blank=True)             # rfu, query form to run before graph
    page_format = models.CharField(max_length=4,
                                   choices=PAGE_FORMATS,
                                   default='html',
                                   blank=True)
    page = models.TextField()           # text of the page with graphs embeded a la django template
    query = models.TextField()          # some django/python to get data for the page

    class Meta:
        verbose_name = "Graph Page"
        verbose_name_plural = "Graph Page"

    def __unicode__(self):
        return u'{}'.format(self.name)
