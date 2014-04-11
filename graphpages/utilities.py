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
import collections

from django.conf import settings
from django.template import add_to_builtins
from django.template.loader import render_to_string
from django.template import Context, Template
from django.utils.encoding import force_unicode


########################################################################################################################

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

########################################################################################################################

# fixme: finish syslog cruft.  add iterator on nodes.  add the last 2 things JZ did, build as a method
# todo 1: add syslog example with form for selecting node and dt range
# todo 1: add extension to allow include from db models
# todo 1: add convenience menthod for add row, add graph, insert row/graph, delete row/graph etc.
# todo 1: need test methods for utilities XGraph...
# todo 1: add link button(s) to each class type
# todo 1: add accordion option to row definition with optional expansion
# todo 1: add support for direct highchart interface
# todo 1: add support for ajax interface for highcharts
# todo 1: add popup window feature to all graph pages and for graph objects

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


class XGraphCell(object):
    """
    Base class for the XGraph... classes.  The XGraph... classes really only provide some syntactic suggar
    for users.

    This class actually does the heavy lifting.  It contains a Graph cell.  The cell may hold graph page, or
    a row of graph columns, or a column of graphs instances, or a graph proper, or ... .  Any XGraph object
    that has a render method can be in an XGraphCell.
    """

    def __init__(self, before_html, after_html, objs=None, width=12, text_before=None, text_after=None):
        """
        Initialize the XGraphCell.

        :param before_html: HTML to output before this cell
        :type before_html: unicode
        :param after_html: HTML to output after this cell
        :type after_html: unicode
        :param objs: The object(s) in this graph.
        :type objs: list or XGraphCell or XGraphPage or XGraphRow or XGColumn or XGraphCK or XGraphHC
        :param width: width of cell (Bootstrap3 width, 1 - 12)
        :type width: int
        :param text_before: Markdown text to display before the graphs on this page.
        :type text_before: unicode
        :param text_after: Markdown text to display after the graphs on this page.
        :type text_after: unicode
        """
        self.before_html = before_html
        self.after_html = after_html
        self.objs = []
        if objs:
            self.col = objs                     # graph objects in this cell
        self.width = width                      # width of this column
        self.text_before = text_before          # markdown text to output before the row
        self.text_after = text_after            # markdown text to output after the row
        pass

    def render(self):
        """
        Generate the html for this graph cell.  Subclass may override this method.
        """
        output = self.before_html
        if self.text_before:
            output += MARKDOWN_TEXT_TEMPLATE.render(Context({'markdown_text': process_markdown(self.text_before)}))
            pass

        # if whatever is in objs is iterable, iterate over the objects and render each according to whatever it is
        # otherwise, just render whatever it is
        if isinstance(self.objs, collections.Iterable):
            for obj in self.objs:
                output += obj.render()
        else:
            output += self.objs.render()

        if self.text_after:
            output += MARKDOWN_TEXT_TEMPLATE.render(Context({'markdown_text': process_markdown(self.text_after)}))
        output += self.after_html
        return output

########################################################################################################################

# This text is used as a wrapper for a graphpage
GRAPHPAGE_BEFORE_HTML = """
<!-- Start of graphpage -->
<div class="container-fluid>
"""

GRAPHPAGE_AFTER_HTML = """
</div>
<!-- End of graphpage -->
"""


class XGraphPage(XGraphCell):
    """
    Graphpage class.  Semantically, this represents a collection of rows of columns of graphs on a page.

    row_________________________________________________________________________________________________
    col________________________ col__________________________ col_______________________________________
    graph______________________ graph________________________ graph_____________________________________
    graph______________________ graph________________________ graph_____________________________________
    graph______________________                               graph_____________________________________
    graph______________________                               graph_____________________________________
    graph______________________
    graph______________________
    row_____________________________________________________________________
    col__________________________ col_______________________________________
    graph________________________ graph_____________________________________

    Columns need not hold the same number of graphs!
    """

    def __init__(self, objs=None, width=12, text_before=None, text_after=None):
        """
        Initialize XGraphPage.

        :param objs: The object(s) in this graph.
        :type objs: list, XGraphRow, XGraphColumn, XGraph
        :param width: width of cell (Bootstrap3 width, 1 - 12)
        :type width: int
        :param text_before: Markdown text to display before the graphs on this page.
        :type text_before: unicode
        :param text_after: Markdown text to display after the graphs on this page.
        :type text_after: unicode
        """
        graphpage_before_html = GRAPHPAGE_BEFORE_HTML.replace('WIDTH', str(width))
        graphpage_after_html = GRAPHPAGE_AFTER_HTML
        super(XGraphPage, self).__init__(graphpage_before_html, graphpage_after_html,
                                         objs, width, text_before, text_after)
        pass

########################################################################################################################

# This text is used as a wrapper for a graphpage row
GRAPHROW_BEFORE_HTML = """
<!-- Start of graphpage row -->
<div class="row">
"""

GRAPHROW_AFTER_HTML = """
</div>
<!-- End of graphpage row -->
"""


class XGraphRow(XGraphCell):
    """
    Graph row class.  Semantically this holds a list of columns of graphs in a row.  See XGraphPage.
    """

    def __init__(self, objs=None, width=12, text_before=None, text_after=None):
        """
        Initialize XGraphRow.

        :param objs: The object(s) in this graph.
        :type objs: list, XGraphRow, XGraphColumn, XGraph
        :param width: width of cell (Bootstrap3 width, 1 - 12)
        :type width: int
        :param text_before: Markdown text to display before the graphs on this page.
        :type text_before: unicode
        :param text_after: Markdown text to display after the graphs on this page.
        :type text_after: unicode
        """
        graphrow_before_html = GRAPHROW_BEFORE_HTML.replace('WIDTH', str(width))
        graphrow_after_html = GRAPHROW_AFTER_HTML
        super(XGraphRow, self).__init__(graphrow_before_html, graphrow_after_html,
                                        objs, width, text_before, text_after)
        pass


########################################################################################################################

# This text is used as a wrapper for a graphpage column
GRAPHCOL_BEFORE_HTML = """
<!-- Start of graphpage column -->
<div class="col-xs-WIDTH col-sm-WIDTH col-md-WIDTH col-lg-WIDTH">
"""

GRAPHCOL_AFTER_HTML = """
</div>
<!-- End of graphpage column -->
"""


class XGraphColumn(XGraphCell):
    """
    Graph column class.  Semantically this holds a list of graphs in a column in a row.
    """
    def __init__(self, objs=None, width=12, text_before=None, text_after=None):
        """
        Create graph column object to hold objects in this column

        :param objs: List of Graph objects in this column.
        :type objs: list, XGraph
        :param width: width of column
        :type width: int
        :param text_before: Markdown text to display before the row.
        :type text_before: unicode
        :param text_after: Markdown text to display after the row.
        :type text_after: unicode
        """
        graphcol_before_html = GRAPHCOL_BEFORE_HTML.replace('WIDTH', str(width))
        graphcol_after_html = GRAPHCOL_AFTER_HTML
        super(XGraphColumn, self).__init__(graphcol_before_html, graphcol_after_html,
                                           objs, width, text_before, text_after)
        pass


########################################################################################################################

# This text is used as a wrapper for a graphpage graph
GRAPH_BEFORE_HTML = """
<!-- Start of graph -->
<div class="row">
    <div class="col-xs-WIDTH col-sm-WIDTH col-md-WIDTH col-lg-WIDTH">
"""

GRAPH_AFTER_HTML = """
    </div>
</div>
<!-- End of graph -->
"""

# This text is used as a wrapper for chartkick template tags
CHARTKICK_BEFORE_HTML = """
<!-- Start of chartkick graph -->
<div class="row">
    <div class="col-xs-12 col-sm-12 col-md-12 col-lg-12">
"""

CHARTKICK_AFTER_HTML = """
    </div>
</div>
<!-- End of chartkick graph -->
"""

LEGAL_GRAPH_TYPES = ['line', 'pie', 'column', 'bar', 'area']


class XGraphCK(object):
    """
    Graph object class.  Class that actually holds the graph object definition.
    """
    def __init__(self, graph_type, data, options=None,
                 width=12, text_before=None, text_after=None):
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
        self.options = options                          # chartkick with options
        self.width = width
        self.text_before = text_before                  # markdown text to display before the graph
        self.text_after = text_after                    # markdown text to display after the graph

        #
        #  Generate the html to render this graph with this data
        #

        # Generate the row for the graph within it's containing col
        output = GRAPH_BEFORE_HTML.replace('WIDTH', str(width))

        # Output text_before if there is any
        if text_before:
            output += MARKDOWN_TEXT_TEMPLATE.render(Context({'markdown_text': process_markdown(text_before)}))
            pass

        # Output the chartkick graph
        if options:
            chart = '{}_chart {} with {}'.format(graph_type, data, options)
            pass
        else:
            chart = '{}_chart {}'.format(graph_type, data)
            pass
        chart = '{% ' + chart + ' %}'
        chart = CHARTKICK_BEFORE_HTML + chart + CHARTKICK_AFTER_HTML

        output += chart

        # Output text_after if there is any
        if text_after:
            output += MARKDOWN_TEXT_TEMPLATE.render(Context({'markdown_text': process_markdown(text_after)}))

        output += GRAPH_AFTER_HTML
        self.output = output
        pass

    def render(self):
        """
        Render the graph
        """
        return self.output

########################################################################################################################


def process_markdown(value):
    """
    Process markdown.
    :param value: The text to process as markdown
    :type value: unicode, the value to process
    :return: HTML version of the markdown text.
    :rtype: unicode, html result from markdown processing
    """
    # extensions = []
    extensions = ["nl2br", ]                    # enable new line to break extension
    # todo 2: review other markdown extensions and enable as appropriate

    return markdown.markdown(force_unicode(value),
                             extensions,
                             output_format='html5',
                             safe_mode=False,
                             enable_attributes=False)
