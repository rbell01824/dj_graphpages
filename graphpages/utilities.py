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
from django.template.loader import render_to_string
from django.template import Context, Template

LEGAL_GRAPH_TYPES = ['line', 'pie', 'column', 'bar', 'area']

# This templte is used to render markdown text full width in a col div.
MARKDOWN_TEXT_TEMPLATE = Template("""<div class="row">
                                         <div class="col-xs-12 col-sm-12 col-md-12 col-lg-12">
                                             {{ markdown_text | graphpage_markdown }}
                                         </div>
                                     </div>
                                  """)

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
        self.text_before = text_before  # markdown text to output before all the graphs on the page
        self.text_after = text_after  # markdown text to output after all the graphs on the page
        self.rows = rows  # rows of graphs on the page
        pass

    def render(self):
        """
        Generate the html for this graph page
        """
        # fixme: generate html for graph page
        output = ''
        if self.text_before:
            output += self.text_before
        for r in self.rows:
            output += r.render()
        if self.text_after:
            output += self.text_after
        return output


class Graph(object):
    """
    Class that holds a single graph definition.
    """

    def __init__(self, graph_type, graph_options=''):
        """
        Create a graph object

        :param graph_type: The type of this graph.  Must be line, pie, column, bar, or area.
        :type graph_type: unicode
        :param graph_options: 'with' options for the chartkick graph.
        :type graph_options: unicode
        """
        if not graph_type in LEGAL_GRAPH_TYPES:
            raise ValueError('In Graph illegal graph type {}'.format(graph_type))
        self.graph_type = graph_type
        self.graph_options = graph_options
        pass

    def render(self, data):
        """
        Generate the html to render this graph with this data.
        """
        if self.graph_options:
            output = "{% {} {} width {}".format(self.graph_type, data, self.graph_options)
        else:
            output = '{% {}_chart {} %}'.format(self.graph_type, data)
        return output


class GraphRow(object):
    """
    Holds a graph row, ie. a list of GraphInstance objects
    """

    def __init__(self, text_before=None, text_after=None, row=list()):
        self.text_before = text_before  # markdown text to output before the row
        self.text_after = text_after  # markdown text to output after the row
        self.row = row  # graphs in the row
        pass

    def render(self):
        """
        Generate the HTML to display this graph row.
        """
        output = ''
        if self.text_before:
            output += MARKDOWN_TEXT_TEMPLATE.render(Context({'markdown_text': self.text_before}))
            pass
        for graph_instance in self.row:
            output += graph_instance.render()
        if self.text_after:
            output += MARKDOWN_TEXT_TEMPLATE.render(Context({'markdown_text': self.text_after}))
        return output


class GraphInstance(object):
    """
    Bound instance of a graph.  That is a graph with its data, width, etc.
    """

    def __init__(self, graph_object, data, width=12, text_before=None, text_after=None):
        self.graph = graph_object  # the graph object to display
        self.data = data  # the data to display
        # set the width of the graph to display
        self.width = 'col-xs-xxx col-sm-xxx col-md-xxx col-lg-xxx'
        self.width.replace('xxx', str(width))
        self.text_before = text_before  # markdown text to display before the graph
        self.text_after = text_after  # markdown text to display after the graph
        self.rendered = graph_object.render(data)
        pass

    def render(self):
        """
        Generate the HTML needed to display this graph.
        """
        # fixme: rewrite to work like graph row
        output = render_to_string('graph_instance.html', {'obj': self})
        return output
