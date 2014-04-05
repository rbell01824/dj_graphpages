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
