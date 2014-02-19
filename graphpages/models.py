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


class GraphPage(models.Model):
    """
    graph page
    """
    name = models.CharField(max_length=50)
    description = models.TextField()
    form = models.TextField()
    page = models.TextField()
    query = models.TextField()

    class Meta:
        verbose_name = "Graph Page"
        verbose_name = "Graph Page"

    def __unicode__(self):
        return u'{}'.format(self.name)
