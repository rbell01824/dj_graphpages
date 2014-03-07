#!/usr/bin/env python
# coding=utf-8

""" Graphpage custom template tags.

2/23/14 - Initial creation

"""

from __future__ import unicode_literals
import logging

log = logging.getLogger(__name__)

__author__ = 'richabel'
__date__ = '2/23/14'
__license__ = "All rights reserved"
__version__ = "0.1"
__status__ = "dev"

from django import template
from django.utils.translation import gettext_lazy as _
from django.template.base import Context, Node

# These are needed inside the exec for the form tag
# noinspection PyUnresolvedReferences
from django import forms
# noinspection PyUnresolvedReferences
from crispy_forms.helper import FormHelper
# noinspection PyUnresolvedReferences
from crispy_forms.layout import Submit
from crispy_forms.utils import render_crispy_form

import re

register = template.Library()

#
# see: https://djangosnippets.org/snippets/9/
#
# This tag can be used to calculate a python expression, and save it into a
# template variable which you can reuse later or directly output to template.
# So if the default django tag can not be suit for your need, you can use it.
#
# How to use it
#
# {% expr "1" as var1 %}
# {% expr [0, 1, 2] as var2 %}
# {% expr _('Menu') as var3 %}
# {% expr var1 + "abc" as var4 %}
# ...
# {{ var1 }}
# for 0.2 version
#
# {% expr 3 %}
# {% expr "".join(["a", "b", "c"]) %}
# Will directly output the result to template
#
# Syntax
#
# {% expr python_expression as variable_name %}
# python_expression can be valid python expression, and you can even
# use _() to translate a string. Expr tag also can used context variables.
#


class ExprNode(template.Node):
    def __init__(self, expr_string, var_name):
        self.expr_string = expr_string
        self.var_name = var_name

    def render(self, context):
        try:
            clist = list(context)
            clist.reverse()
            # noinspection PyDictCreation
            d = {}
            d['_'] = _
            for c in clist:
                for item in c:
                    if isinstance(item, dict):
                        d.update(item)
            if self.var_name:
                # context[self.var_name] = eval(self.expr_string, d)
                # context.dicts[0][self.varname] = eval(self.expr_string, d)
                # todo 2: this is a hack to run in the global context, fixme fixme fixme
                # context.dicts[0][self.varname] = eval(self.expr_string)
                context[self.var_name] = eval(self.expr_string)
                return ''
            else:
                return str(eval(self.expr_string, d))
        except:
            raise
        pass

r_expr = re.compile(r'(.*?)\s+as\s+(\w+)', re.DOTALL)


# noinspection PyUnusedLocal
def do_expr(parser, token):
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires arguments" % token.contents[0]
    m = r_expr.search(arg)
    if m:
        expr_string, var_name = m.groups()
    else:
        if not arg:
            raise template.TemplateSyntaxError, "%r tag at least require one argument" % tag_name

        expr_string, var_name = arg, None
    return ExprNode(expr_string, var_name)
do_expr = register.tag('expr', do_expr)

# todo 2: resolve this
# kunitoki (on June 9, 2010):
# This doesn't work inside template blocks in inherited templates
# (will give errors in dict.update). This update in the node will work on both places:
#
# class ExprNode(template.Node):
#     def __init__(self, expr_string, var_name):
#         self.expr_string = expr_string
#         self.var_name = var_name
#
#     def render(self, context):
#         try:
#             clist = list(context)
#             clist.reverse()
#             d = {}
#             d['_'] = _
#             for c in clist:
#                 for item in c:
#                     if isinstance(item, dict):
#                         d.update(item)
#             if self.var_name:
#                 context[self.var_name] = eval(self.expr_string, d)
#                 return ''
#             else:
#                 return str(eval(self.expr_string, d))
#         except:
#             raise
# #
#
# sjohnson (on December 15, 2011):
# To use the value outside of the block (e.g., outside of the for loop) in
# which it is set, use
#
# context.dicts[0][self.varname] = eval(self.expr_string, d)
#
# (You could reconfigure the regex to check for "as global" or "as" and set
# the variable appropriately)
#

###############################################################################


# noinspection PyUnusedLocal
@register.tag(name='form')
def do_form(parser, token):
    """
    Stops the template engine from rendering the contents of this block tag.

    Usage::

        {% form %}
            form class definition goes here
        {% endform %}

     Example::
        {% form no_countries %}
        class GraphForm(forms.Form):
            title = forms.CharField(min_length=3, max_length=80, label='Title')
            number_countries = forms.IntegerField(max_value=50, min_value=5,
                                                  label='Number of countries')
            helper = FormHelper()
            helper.form_method = 'POST'
            helper.add_input(Submit('submit', 'Show graph', css_class='btn-primary'))
        {% endform no_countries %}

    You can also designate a specific closing tag block (allowing the
    unrendered use of ``{% endform %}``)::

        {% form myblock %}
            ...
        {% endform myblock %}
    """
    nodelist = parser.parse(('endform',))
    parser.delete_first_token()
    return FormNode(nodelist.render(Context()))


class FormNode(template.Node):
    def __init__(self, content):
        self.content = content

    def render(self, context):
        # When we get here, self.content has the form definition.  We need to turn it into html.
        exec(self.content, globals(), locals())
        # noinspection PyUnresolvedReferences
        unbound_form = GraphForm()
        rtn = render_crispy_form(unbound_form)
        return rtn


# noinspection PyUnusedLocal
@register.tag(name='query')
def do_query(parser, token):
    """
    Stops the template engine from rendering the contents of this block tag.

    Usage::

        {% query %}
            {% don't process this %}
        {% endquery %}

    You can also designate a specific closing tag block (allowing the
    unrendered use of ``{% endquery %}``)::

        {% query myblock %}
            ...
        {% endquery myblock %}
    """
    nodelist = parser.parse(('endquery',))
    parser.delete_first_token()
    return QueryNode(nodelist.render(Context()))


class QueryNode(Node):
    def __init__(self, content):
        self.content = content

    def render(self, context):
        return self.content
