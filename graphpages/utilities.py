#!/usr/bin/env python
# coding=utf-8

""" Some description here

3/31/14 - Initial creation

"""

from __future__ import unicode_literals
import logging

log = logging.getLogger(__name__)

__author__ = 'richabel'
__date__ = '3/31/14'
__license__ = "All rights reserved"
__version__ = "0.1"
__status__ = "dev"

from django.conf import settings
from django.template import add_to_builtins

LEGAL_GRAPH_TYPES = ['line', 'pie', 'column', 'bar', 'area']


def load_templatetags():
    """
    Load custom template tags so they are always available.  See https://djangosnippets.org/snippets/342/.

    In your settings file:

    TEMPLATE_TAGS = ( "djutils.templatetags.sqldebug", )

    Make sure load_templatetags() gets called somewhere, for example in your apps init.py
    """
    # This is important: If the function is called early, and some of the custom
    # template tags use superclasses of django template tags, or otherwise cause
    # the following situation to happen, it is possible that circular imports
    # cause problems:
    #
    # If any of those superclasses import django.template.loader (for example,
    # django.template.loader_tags does this), it will immediately try to register
    # some builtins, possibly including some of the superclasses the custom template
    # uses. This will then fail because the importing of the modules that contain
    # those classes is already in progress (but not yet complete), which means that
    # usually the module's register object does not yet exist.
    #
    # In other words:
    #       {custom-templatetag-module} ->
    #       {django-templatetag-module} ->
    #       django.template.loader ->
    #           add_to_builtins(django-templatetag-module)
    #           <-- django-templatetag-module.register does not yet exist
    #
    # It is therefor imperative that django.template.loader gets imported *before*
    # any of the templatetags it registers.
    #

    from django.template.loader import add_to_builtins

    #
    # Note: For reasons I don't understand this code gets ececuted twice when
    # Django starts.  Nothing bad seems to happen so I'll use the technique.
    # print '=== in utilities init ==='
    #
    # Register the template tag as <application>.templatetags.<template tag lib>
    #
    try:
        for lib in settings.TEMPLATE_TAGS:
            add_to_builtins(lib)
    except AttributeError:
        pass


class GraphPage(object):
    """
    Graphpage class.  This allows use of class methods to create a graphpage.
    """

    def __init__(self, text_before=None, text_after=None, rows=list):
        self.text_before = None             # markdown text to output before all the graphs on the page
        self.text_after = None              # markdown text to output after all the graphs on the page
        self.rows = []                      # rows of graphs on the page
        # self.graphs = {}                    # graphs on the page
        pass

    def text_top(self, text):
        """
        Save markdown text to output before any graphs on the page.

        :param text: Markdown text to output before any graphs on the page.
        :type text: unicode
        :return: Nothing
        :rtype: None
        """
        self.text_top = text
        return

    def text_bottom(self, text):
        """
        Save markdown text to output after last graph on the page.

        :param text: Markdown text to output after last graph on the page.
        :type text: unicode
        :return: Nothing
        :rtype: None
        """
        self.text_bottom = text
        return

    def graph_create(self, graph_name, graph_type='column', graph_with_options=''):
        """
        Create a graph object on the page.

        :param graph_name: The name of the graph.  Must be unique within the graphpage.
        :type graph_name: unicode
        :param graph_type: The type of this graph.  Must be line, pie, column, bar, or area.
        :type graph_type: unicode
        :param graph_with_options: 'with' options for the chartkick graph.
        :type graph_with_options: unicode
        :return: Graph object created
        :rtype: Graph
        """
        # Create the graph object
        graph_object = Graph(graph_name, graph_type, graph_with_options)

        # Save if possible
        return graph_object

    def graph_add(self, graph_object):
        """
        Add a graph object to the page.

        :param graph_object: The graph object to add to the page.
        :type graph_object: Graph
        :return: Graph object
        :rtype: Graph
        """
        # check if one already exists
        if graph_object.graph_name in self.graphs:
            raise ValueError('In graph_add duplicate graph name {}.'.format(graph_object.graph_name))

        # save it
        self.graphs[graph_object.graph_name] = graph_object
        return graph_object


class Graph(object):
    """
    Class that holds a single graph definition.
    """
    def __init__(self, graph_name, graph_type, graph_with_options=''):
        """
        Create a graph object

        :param graph_name: The name of the graph.  Must be unique within the graphpage.
        :type graph_name: unicode
        :param graph_type: The type of this graph.  Must be line, pie, column, bar, or area.
        :type graph_type: unicode
        :param graph_with_options: 'with' options for the chartkick graph.
        :type graph_with_options: unicode
        """

        self.graph_name = graph_name
        if not graph_type in LEGAL_GRAPH_TYPES:
            raise ValueError('In Graph illegal graph type {}'.format(graph_type))
        self.graph_type = graph_type
        self.graph_with_options = graph_with_options
        pass


class GraphRow(object):
    """
    Holds a graph row.
    """
    def __init__(self):
        self.row = []                       # graphs in the row
        self.text_before = None             # text to output before the row
        self.text_after = None              # text to output after the row
        pass


class GraphInstance(object):
    """
    Bound instance of a graph.  That is a graph with its data, width, etc.
    """
    def __init__(self, graph_object, data, width=12, text_before=None, text_after=None):
        self.graph = graph_object               # the graph object to display
        self.data = data                        # the data to display
        self.width = width                      # the width of the graph to display
        self.text_before = text_before          # markdown text to display before the graph
        self.text_after = text_after            # markdown text to display after the graph
        pass
