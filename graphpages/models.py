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

# Basic taggit manager
# from taggit.managers import TaggableManager

# Autosuggest from existing tag list
# see https://bitbucket.org/fabian/django-taggit-autosuggest
from taggit_autosuggest.managers import TaggableManager


class GraphPageTags(models.Model):
    tag = models.CharField(max_length=20, unique=True)
    description = models.TextField()

    class Meta:
        verbose_name = "Graph Page Tags"
        verbose_name_plural = "Graph Page Tags"

    def __unicode__(self):
        return u'{}'.format(self.tag)


class GraphPageGraph(models.Model):
    name = models.CharField(max_length=200,
                            blank=False,
                            unique=True)
    description = models.TextField(blank=True)
    my_tags = models.ManyToManyField(GraphPageTags,
                                     blank=True,
                                     null=True)
    tags = TaggableManager()
    # The actual form
    form = models.TextField(blank=True)
    form_ref = models.ForeignKey('self', related_name='fk_form',
                                 default=None, blank=True, null=True)
    # The page the form is on
    form_page = models.TextField(blank=True)
    form_page_ref = models.ForeignKey('self', related_name='fk_form_page',
                                      default=None, blank=True, null=True)
    # The Django/python to get the form data
    query = models.TextField(blank=True)
    query_ref = models.ForeignKey('self', related_name='fk_query',
                                  default=None, blank=True, null=True)
    # The page the form data is displayed on
    template = models.TextField(blank=True)
    template_ref = models.ForeignKey('self', related_name='fk_template',
                                     default=None, blank=True, null=True)

    class Meta:
        verbose_name = "GraphPage Graph"
        verbose_name_plural = "GraphPage Graph"

    def __unicode__(self):
        return u'{}'.format(self.name)
    pass
