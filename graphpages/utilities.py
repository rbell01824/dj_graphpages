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

import markdown

from django.conf import settings
from django.template import add_to_builtins
from django.template.loader import render_to_string
from django.template import Context, Template
from django.utils.encoding import force_unicode

LEGAL_GRAPH_TYPES = ['line', 'pie', 'column', 'bar', 'area']

# This template is used to render markdown text full width in a col div.
MARKDOWN_TEMPLATE_TEXT = """
<!-- Start of textbefore/after -->
<div class="row">
    <div class="col-xs-12 col-sm-12 col-md-12 col-lg-12">
        {{ markdown_text|safe }}
    </div>
</div>
<!-- End of textbefore/after -->
"""
MARKDOWN_TEXT_TEMPLATE = Template(MARKDOWN_TEMPLATE_TEXT)

# This text is used as a wrapper for a graphpage
GRAPHPAGE_BEFORE_TEXT = """
<!-- Start of graphpage -->
<div class="row">
    <div class="col-xs-12 col-sm-12 col-md-12 col-lg-12">
"""
GRAPHPAGE_AFTER_TEXT = """
    </div>
</div>
<!-- End of graphpage -->
"""

# This text is used as a wrapper for a graphpage row
GRAPHROW_BEFORE_TEXT = """
<!-- Start of row -->
<div class="row">
    <div class="col-xs-12 col-sm-12 col-md-12 col-lg-12">
"""
GRAPHROW_AFTER_TEXT = """
    </div>
</div>
<!-- End of row -->
"""

# This text is used as a wrapper for a graphpage row graph cell
GRAPH_BEFORE_TEXT = """
<!-- Start of graph -->
<div class="{}">
"""
GRAPH_AFTER_TEXT = """
</div>
<!-- End of graph -->
"""

# This text is used as a wrapper for chartkick template tags
CHARTKICK_BEFORE_TEXT = """
<!-- Start of chartkick graph -->
<div class="row">
    <div class="col-xs-12 col-sm-12 col-md-12 col-lg-12">
"""
CHARTKICK_AFTER_TEXT = """
    </div>
</div>
<!-- End of chartkick graph -->
"""


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

# todo 1: add extension to allow include from db models
# todo 1: add convenience menthod for add row, add graph, insert row/graph, delete row/graph etc.
# todo 1: need test methods for utilities XGraph...
# todo 1: add link button(s) to each class type
# todo 1: add support for direct highchart interface
# todo 1: add support for ajax interface for highcharts
# todo 1: get large timebase data set to demo with
# todo 1: add popup window feature to all graph pages and for graph objects

class XGraphPage(object):
    """
    Graphpage class.  This allows use of class methods to create a graphpage.
    """

    def __init__(self, rows=list(), text_before=None, text_after=None):
        """
        Initialize graphpage.
        :param rows: The rows in this graph.
        :type rows: list
        :param text_before: Markdown text to display before the graphs on this page.
        :type text_before: unicode
        :param text_after: Markdown text to display after the graphs on this page.
        :type text_after: unicode
        """
        self.rows = rows                        # rows of graphs on the page
        self.text_before = text_before          # markdown text to output before all the graphs on the page
        self.text_after = text_after            # markdown text to output after all the graphs on the page
        pass

    def render(self):
        """
        Generate the html for this graph page.
        """
        output = GRAPHPAGE_BEFORE_TEXT
        if self.text_before:
            output += MARKDOWN_TEXT_TEMPLATE.render(Context({'markdown_text': process_markdown(self.text_before)}))
            pass
        # noinspection PyTypeChecker
        for r in self.rows:
            output += r.render()
        if self.text_after:
            output += MARKDOWN_TEXT_TEMPLATE.render(Context({'markdown_text': process_markdown(self.text_after)}))
        output += GRAPHPAGE_AFTER_TEXT
        return output


class XGraphRow(object):
    """
    Holds a graph row, ie. a list of GraphInstance objects
    """

    def __init__(self, row=list(), text_before=None, text_after=None):
        """
        Create graph row object to hold graphs in this row.

        :param row: List of Graph objects in this row.
        :type row: list
        :param text_before: Markdown text to display before the row.
        :type text_before: unicode
        :param text_after: Markdown text to display after the row.
        :type text_after: unicode
        """
        self.row = row                          # graphs in the row
        self.text_before = text_before          # markdown text to output before the row
        self.text_after = text_after            # markdown text to output after the row
        pass

    def render(self):
        """
        Generate the HTML to display this graph row.
        """
        output = GRAPHROW_BEFORE_TEXT
        if self.text_before:
            output += MARKDOWN_TEXT_TEMPLATE.render(Context({'markdown_text': process_markdown(self.text_before)}))
            pass
        for graph_instance in self.row:
            output += graph_instance.output
        if self.text_after:
            output += MARKDOWN_TEXT_TEMPLATE.render(Context({'markdown_text': process_markdown(self.text_after)}))
        output += GRAPHROW_AFTER_TEXT
        return output


class XGraph(object):
    """
    Class that holds a single graph definition.
    """
    def __init__(self, graph_type, data,
                 options=None, width=12, text_before=None, text_after=None):
        """
        Create a graph object

        :param graph_type: The type of this graph.  Must be line, pie, column, bar, or area.
        :type graph_type: unicode
        :param data: The name of the context variable holding the graph's data
        :type data: unicode
        :param options: 'with' options for the chartkick graph.
        :type options: unicode
        :param width: Bootstrap3 grid width for graph
        :type width: int
        :param text_before: Markdown text to display before the graph.
        :type text_before: unicode
        :param text_after: Markdown text to display after the graph.
        :type text_after: unicode
        """

        if not graph_type in LEGAL_GRAPH_TYPES:
            raise ValueError('In Graph illegal graph type {}'.format(graph_type))
        # todo 2: when this is working, remove the unneeded class attributes since all that's really needed is self.output
        self.graph_type = graph_type                    # save type of graph
        self.data = data                                # the data to display
        self.options = options                          # chartkick with otions
        # set the width of the graph to display
        width_ = 'col-xs-xxx col-sm-xxx col-md-xxx col-lg-xxx'
        self.width = width_.replace('xxx', str(width))
        self.text_before = text_before                  # markdown text to display before the graph
        self.text_after = text_after                    # markdown text to display after the graph

        #
        #  Generate the html to render this graph with this data
        #
        # Output text_before if there is any
        #
        output = GRAPH_BEFORE_TEXT.format(self.width)
        # todo 1: markdown text must be safe
        if text_before:
            output += MARKDOWN_TEXT_TEMPLATE.render(Context({'markdown_text': process_markdown(text_before)}))
            pass

        #
        # Output the chartkick graph
        #
        if options:
            chart = '{}_chart {} with {}'.format(graph_type, data, options)
            pass
        else:
            chart = '{}_chart {}'.format(graph_type, data)
            pass
        chart = '{% ' + chart + ' %}'
        chart = CHARTKICK_BEFORE_TEXT + chart + CHARTKICK_AFTER_TEXT

        output += chart

        #
        # Output text_after if there is any
        #
        if text_after:
            output += MARKDOWN_TEXT_TEMPLATE.render(Context({'markdown_text': process_markdown(text_after)}))

        output += GRAPH_AFTER_TEXT
        self.output = output
        pass


def process_markdown(value):
    """
    Process markdown.
    :param value: The text to process as markdown
    :type value: unicode, the value to process
    :return: HTML version of the markdown text.
    :rtype: unicode, html result from markdown processing
    """
    extensions = ["nl2br", ]                    # enable new line to break extension
    # todo 2: review other markdown extensions and enable as appropriate

    return markdown.markdown(force_unicode(value),
                             extensions,
                             output_format='html5',
                             safe_mode=True,
                             enable_attributes=False)
