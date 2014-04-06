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

# These are needed inside the exec for the form tag and crispy
# noinspection PyUnresolvedReferences
from django import forms

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

# todo 2: clean up this code, it's not actually used right now but may come in handy so save for a bit

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
