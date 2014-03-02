#!/usr/bin/env python
# coding=utf-8

""" Some description here

3/2/14 - Initial creation

"""

# from __future__ import unicode_literals
import logging

log = logging.getLogger(__name__)

__author__ = 'richabel'
__date__ = '3/2/14'
__license__ = "All rights reserved"
__version__ = "0.1"
__status__ = "dev"

__author__ = 'rbell01824'

from django import forms

print '======================== define form class and eval doesn\'t work'

xxx = """
class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField()
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)
"""

print xxx
print """
But
zzz = eval(xxx)
print zzz

gives a syntax error.
"""

print '======================== define form class and exec does not'

exec(xxx)
# noinspection PyUnresolvedReferences
form = ContactForm()
print form

print '======================== define fields as variables works for most any field'
name = forms.TextInput(attrs={'size': 10, 'title': 'Your name',})
print name.render('aaa', 'bbb')
print name.render('ccc', 'ddd')
subject = forms.CharField(max_length=100)
print subject.widget.render('aaa', 'bbb')
message = forms.CharField()
print message.widget.render('aaa', 'bbb')
sender = forms.EmailField()
print sender.widget.render('aaa', 'bbb')
cc_myself = forms.BooleanField(required=False)
print cc_myself.widget.render('aaa', 'bbb')


print '======================== here\'s what happend playing in the normal way'
class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField()
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)

print '======================== contact form class'
form = ContactForm()
print form
print '======================== contact form class as_...'
print form.as_p()
print form.as_table()

print '======================== here\'s another solution'
print """
----------------------------------------------------------------
how to generate a dynamic at runtime form in Django
----------------------------------------------------------------
idea taken from http://www.b-list.org/weblog/2008/nov/09/dynamic-forms/
"""

def make_form(class_name, fields):
    return type(class_name, (forms.BaseForm,), { 'base_fields': fields })

print '======================== contact form from list of fields 2 ======================== '
form3_class = make_form('foo', { 'name': forms.CharField(max_length=50),
                                 'email': forms.EmailField(),
                                 'message': forms.CharField(widget=forms.Textarea) })
print form3_class()
print '------------------------------------------------------------------------------------'
print form3_class().as_p()
print '------------------------------------------------------------------------------------'
print form3_class.__name__, form3_class.__bases__, form3_class.__dict__
print '------------------------------------------------------------------------------------'
print type(form3_class())
print '------------------------------------------------------------------------------------'

print '======================== contact form from list of fields 3 ======================== '
form4_class = type('foo4', (forms.BaseForm,), {'base_fields': { 'name': forms.CharField(max_length=50),
                                                                'email': forms.EmailField(),
                                                                'message': forms.CharField(widget=forms.Textarea) }})
print '------------------------------------------------------------------------------------'
print 'form4\n', form4_class()
print '------------------------------------------------------------------------------------'
print 'form4 as_p\n', form4_class().as_p()
print '------------------------------------------------------------------------------------'

print '======================== contact form from list of fields 4 ======================== '

import collections

def make_form2(fields, class_name='temp_form'):
    xfields = ''
    # field_dict = {}
    lines = fields.split('\n')
    for line in lines:
        line = line.strip()                         # clean spaces
        if len(line) == 0:                          # skip blank lines
            continue
        print '===', line
        parts = line.split(' ', 1)                  # seperate field name and type
        name = parts[0].strip()
        type = 'form.' + parts[1].strip()
        print '<{}><{}>'.format(name, type)
        xfields += ', ' + '\'{}\':forms.{}'.format(name, type)
        print xfields

    # def make_form(class_name, fields):
    #     return type(class_name, (forms.BaseForm,), { 'base_fields': fields })
    form_expr = """rtn = type('%s', (forms.BaseForm,), {'base_fields':{%s}})""" % (class_name, xfields[1:])
    print form_expr
    # local_context = {}
    # global_context = {forms}
    from django import forms

    exec(form_expr)
    return 3


xxx = """
name forms.CharField(max_length=50)
email forms.EmailField()
message     forms.CharField(widget=forms.Textarea)
"""

# form5 = make_form2(xxx)
# print '------------------------------------------------------------------------------------'
# print 'form5\n', form5()
# print '------------------------------------------------------------------------------------'
