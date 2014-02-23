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


class GraphTemplateTags(models.Model):
    tag = models.CharField(max_length=20, unique=True)
    description = models.TextField()

    class Meta:
        verbose_name = "Graph Template Tags"
        verbose_name_plural = "Graph Template Tags"

    def __unicode__(self):
        return u'{}'.format(self.tag)


class GraphTemplates(models.Model):
    name = models.CharField(max_length=50,          # name of template
                            unique=True)
    description = models.TextField(blank=True,      # some sort of useful description
                                   help_text='Description with parameters')
    tags = models.ManyToManyField(GraphTemplateTags,
                                  blank=True,
                                  null=True)
    template = models.TextField(blank=True)         # the actual template

    class Meta:
        verbose_name = "Graph Template"
        verbose_name_plural = "Graph Templates"

    def __unicode__(self):
        return u'{}'.format(self.name)


class GraphPageTags(models.Model):
    tag = models.CharField(max_length=20, unique=True)
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

    name = models.CharField(max_length=50,          # name of graph page
                            unique=True)
    description = models.TextField(blank=True)      # some sort of useful description
    tags = models.ManyToManyField(GraphPageTags,
                                  blank=True,
                                  null=True)
    form = models.TextField(blank=True)             # rfu, query form to run before graph
    page_format = models.CharField(max_length=4,
                                   choices=PAGE_FORMATS,
                                   default='html',
                                   blank=True)
    template = models.ForeignKey(GraphTemplates,    # base template if present
                                 blank=True,
                                 null=True)
    page = models.TextField(blank=True,             # text of the page with graphs embeded a la django template
                            null=True)
    query = models.TextField()                      # some django/python to get data for the page

    class Meta:
        verbose_name = "Graph Page"
        verbose_name_plural = "Graph Page"

    def __unicode__(self):
        return u'{}'.format(self.name)
#
###############################################################################
#
# GraphPage2: improved models
#
###############################################################################
#


class Graph2Tags(models.Model):
    tag = models.SlugField(max_length=20, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Graph2 Tags"
        verbose_name_plural = "Graph2 Tags"

    def __unicode__(self):
        return u'{}'.format(self.tag)


class Graph2Form(models.Model):
    name = models.CharField(max_length=200,
                            blank=False,
                            unique=True)
    description = models.TextField(blank=True)
    tags = models.ManyToManyField(Graph2Tags,
                                  blank=True,
                                  null=True)
    form = models.TextField(blank=False)

    class Meta:
        verbose_name = "Graph2 Form"
        verbose_name_plural = "Graph2 Form"

    def __unicode__(self):
        return u'{}'.format(self.name)
    pass


class Graph2Template(models.Model):
    name = models.CharField(max_length=200,
                            blank=False,
                            unique=True)
    description = models.TextField(blank=True)
    tags = models.ManyToManyField(Graph2Tags,
                                  blank=True,
                                  null=True)
    template = models.TextField(blank=False)

    class Meta:
        verbose_name = "Graph2 Template"
        verbose_name_plural = "Graph2 Template"

    def __unicode__(self):
        return u'{}'.format(self.name)
    pass


class Graph2Query(models.Model):
    name = models.CharField(max_length=200,
                            blank=False,
                            unique=True)
    description = models.TextField(blank=True)
    tags = models.ManyToManyField(Graph2Tags,
                                  blank=True,
                                  null=True)
    query = models.TextField(blank=False)

    class Meta:
        verbose_name = "Graph2 Query"
        verbose_name_plural = "Graph2 Query"

    def __unicode__(self):
        return u'{}'.format(self.name)
    pass


class Graph2Graph(models.Model):
    name = models.CharField(max_length=200,
                            blank=False,
                            unique=True)
    description = models.TextField(blank=True)
    tags = models.ManyToManyField(GraphPageTags,
                                  blank=True,
                                  null=True)
    form = models.ForeignKey(Graph2Form,
                             blank=True,
                             null=True)
    page = models.ForeignKey(Graph2Template,
                             blank=True,
                             null=True)
    query = models.ForeignKey(Graph2Query,
                              blank=True,
                              null=True)

    class Meta:
        verbose_name = "Graph2 Graph"
        verbose_name_plural = "Graph2 Graph"

    def __unicode__(self):
        return u'{}'.format(self.name)
    pass
