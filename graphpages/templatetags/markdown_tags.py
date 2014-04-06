#!/usr/bin/env python
# coding=utf-8

""" Some description here

3/23/14 - Initial creation

"""

from __future__ import unicode_literals
import logging

log = logging.getLogger(__name__)

__author__ = 'richabel'
__date__ = '3/23/14'
__license__ = "All rights reserved"
__version__ = "0.1"
__status__ = "dev"

import markdown

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(is_safe=True)
@stringfilter
def graphpage_markdown(value):
    """
    Process markdown.
    :type value: unicode, the value to process
    :rtype: unicode, html result from markdown processing
    """
    extensions = ["nl2br", ]                    # enable new line to break extension

    return mark_safe(markdown.markdown(force_unicode(value),
                                       extensions,
                                       safe_mode=True,
                                       enable_attributes=False))
# todo 3: look into using markdown2
