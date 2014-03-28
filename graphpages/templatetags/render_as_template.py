#!/usr/bin/env python
# coding=utf-8

""" Renders context variable.

See: https://djangosnippets.org/snippets/1373/
This is a template tag that works like {% include %}, but instead of loading a template
from a file, it uses some text from the current context, and renders that as though it
were itself a template. This means, amongst other things, that you can use template tags
and filters in database fields.

For example, instead of:

{{ context_variable }}

you could use:

{% render_as_template context_variable %}

Then you can use template tags (such as {% url showprofile user.id %}) in flat pages,
stored in the database.

The template is rendered with the current context.

Warning - only allow trusted users to edit content that gets rendered with this tag.
3/28/14 - Initial creation

"""

from __future__ import unicode_literals
import logging

log = logging.getLogger(__name__)

__author__ = 'richabel'
__date__ = '3/28/14'
__license__ = "All rights reserved"
__version__ = "0.1"
__status__ = "dev"

from django import template
from django.template import Template, Variable, TemplateSyntaxError

register = template.Library()


class RenderAsTemplateNode(template.Node):
    """
    Renders variable
    """
    def __init__(self, item_to_be_rendered):
        """
        :param item_to_be_rendered: the item to be rendered, ex. {% piechart %}
        :type item_to_be_rendered: unicode
        """
        self.item_to_be_rendered = Variable(item_to_be_rendered)

    def render(self, context):
        """
        Render variable in context.
        :param context: Current template context.
        :type context: dict
        :return: Rendered variable
        :rtype: unicode
        """
        try:
            actual_item = self.item_to_be_rendered.resolve(context)
            return Template(actual_item).render(context)
        except template.VariableDoesNotExist:
            return ''


def render_as_template(parser, token):
    """

    :param parser:
    :param token:
    :return: :rtype: :raise TemplateSyntaxError:
    """
    bits = token.split_contents()
    if len(bits) != 2:
        raise TemplateSyntaxError("'%s' takes only one argument"
                                  " (a variable representing a template to render)" % bits[0])
    return RenderAsTemplateNode(bits[1])


render_as_template = register.tag(render_as_template)
