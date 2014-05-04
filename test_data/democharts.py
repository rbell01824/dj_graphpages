#!/usr/bin/env python
# coding=utf-8

""" Sources for various demo charts to facilitate editing, testing, and make sure things are in the repo.

5/3/14 - Initial creation

"""

from __future__ import unicode_literals
import logging

log = logging.getLogger(__name__)

__author__ = 'richabel'
__date__ = '5/3/14'
__license__ = "All rights reserved"
__version__ = "0.1"
__status__ = "dev"

from graphpages.utilities import XGraphPage
from graphpages.utilities import XGraphCell
from graphpages.utilities import XGraphRow
from graphpages.utilities import XGraphColumn
from graphpages.utilities import XGraphCK
from graphpages.utilities import XGraphHC

from test_data.models import syslog_query, VNode
from django.db.models import Count

########################################################################################################################
#
# syslog_demo 8a
#
########################################################################################################################


# noinspection PyDocstring
def syslog_demo_8a():

    graphpage = XGraphPage()

    # set the company and node values, ignour start/end date time for now
    company = 'BMC_1'
    node = 'A0040CnBPGC1'

    # Put title and some text on the page
    graphpage.text_before = '\n' \
                            'First Syslog Graphs\n' \
                            '===============\n\n' \
                            'Charts from one month of syslog data.\n\n' \
                            '    * **Notes**\n\n' \
                            '    * Queries copied from JZ code with extensions to create a richer graph ' \
                            'environment.\n\n' \
                            '    * For this demonstration I have chosen to create a single page with ALL of the ' \
                            'syslog results graphs.\n\n' \
                            '    * The test data set has only one company so there is no form for company.\n\n' \
                            '    * The test data set has one month of data.  I chose **NOT** to query for a data ' \
                            'range since query functionality is already well demonstrated.\n\n' \
                            '<br/>\n'

    # get the syslog qs for this company/node
    qs = syslog_query(company, node)

    # Count them all
    all_count_host = qs.count()

    # Count by type
    xqs = qs.values('message_type').annotate(num_results=Count('id'))

    count_by_type_type = map(list, xqs.order_by('message_type').values_list('message_type', 'num_results'))
    count_by_type_count = map(list, xqs.order_by('-num_results').values_list('message_type', 'num_results'))

    graph11 = XGraphCK('column', 'count_by_type_type', width=6)
    graph12 = XGraphCK('pie', 'count_by_type_count', width=6)

    # Put graphs on page
    text_before = '<h3>Company {{company}} Node {{node}} Count by Type Distribution</h3>' \
                  '<p>Total syslog records {{all_count_host}}</p>'

    graphpage.objs.append(XGraphRow([graph11, graph12], text_before=text_before))

    ################################################################################
    #
    # Display summary for all hosts for this company
    #
    ################################################################################

    qs = syslog_query(company)
    all_count = qs.count()

    # Count critical events

    critical_event_count_by_host = map(list, qs.filter(message_type='critical').
                                       order_by('node__host_name').
                                       values('node__host_name').
                                       annotate(count=Count('node__host_name')).
                                       values_list('node__host_name', 'count'))
    critical_event_count_by_host_title = '<h3>Critical Event Count by Host Distribution</h3>'
    graph31 = XGraphCK('column', 'critical_event_count_by_host',
                       width=6,
                       text_before=critical_event_count_by_host_title)
    graph32 = XGraphCK('pie', 'critical_event_count_by_host',
                       width=6,
                       text_before=critical_event_count_by_host_title)
    text_before = '<h3>Company {{company}} All Hosts</h3>' \
                  '<p>Total syslog records {{all_count}}</p>'
    graphpage.objs.append(XGraphRow([graph31, graph32], text_before=text_before))

    # Count error events
    error_event_count_by_host = map(list, qs.filter(message_type='error').
                                    order_by('node__host_name').
                                    values('node__host_name').
                                    annotate(count=Count('node__host_name')).
                                    values_list('node__host_name', 'count'))
    error_event_count_by_host_title = '<h3>Error Event Count by Host Distribution</h3>'
    graph33 = XGraphCK('column', 'error_event_count_by_host',
                       width=6,
                       text_before=error_event_count_by_host_title)
    graph34 = XGraphCK('pie', 'error_event_count_by_host',
                       width=6,
                       text_before=error_event_count_by_host_title)

    # put graphs on page
    graphpage.objs.append(XGraphRow([graph33, graph34]))

    return locals()


########################################################################################################################
#
# syslog_demo 8b
#
########################################################################################################################


# noinspection PyDocstring
def syslog_demo_8b():

    # set the company and node values, ignour start/end date time for now
    company = 'BMC_1'

    # Create graphpage
    graphpage = XGraphPage()

    # Put title and some text on the page
    graphpage.text_before = 'Critical and Error Event Summary for {{ company }}\n' \
                            '==================================================\n'

    ################################################################################
    #
    # Display summary for all hosts for this company
    #
    ################################################################################

    qs = syslog_query(company)
    all_count = qs.count()

    # Count critical events
    critical_event_count = map(list, qs.filter(message_type='critical').
                               order_by('node__host_name').
                               values('node__host_name').
                               annotate(count=Count('node__host_name')).
                               values_list('node__host_name', 'count'))
    critical_event_count_title = '<h3>Critical Event Count by Host</h3>'
    graph31 = XGraphCK('column', 'critical_event_count',
                       width=3,
                       text_before=critical_event_count_title)
    graph32 = XGraphCK('pie', 'critical_event_count',
                       width=3,
                       text_before=critical_event_count_title)
    error_event_count = map(list, qs.filter(message_type='error').
                            order_by('node__host_name').
                            values('node__host_name').
                            annotate(count=Count('node__host_name')).
                            values_list('node__host_name', 'count'))
    error_event_count_title = '<h3>Error Event Count by Host</h3>'
    graph33 = XGraphCK('column', 'error_event_count',
                       width=3,
                       text_before=error_event_count_title)
    graph34 = XGraphCK('pie', 'error_event_count',
                       width=3,
                       text_before=error_event_count_title)
    text_before = "<h3>Company {{company}} All Hosts</h3>" \
                  "<p>Total syslog records {{all_count}}</p>"
    graphpage.objs.append(XGraphRow([graph31, graph32, graph33, graph34], text_before=text_before))

    ################################################################################
    #
    # Display summary for each host for this company
    #
    ################################################################################

    # get the hosts for this company and put it on the page
    hosts = [n[0] for n in VNode.objects.filter(company__company_name=company).values_list('host_name')]
    hosts_text = '<h3>The company has the following hosts: ' + ', '.join(hosts) + '</h3>'
    graphpage.objs.append(XGraphRow(text_before=hosts_text))

    for host in hosts:
        # get the syslog qs for this company/node
        qs = syslog_query(company, host)

        # count and build title
        count = qs.count()
        host_text = '<h3>Company: {} Host: {}</h3>' \
                    '<p>Total syslog records {}</p>' \
            .format(company, host, count)

        # Count by type
        xqs = qs.values('message_type').annotate(num_results=Count('id'))

        count_by_type_type = map(list, xqs.order_by('message_type').values_list('message_type', 'num_results'))
        graph11 = XGraphCK('column', count_by_type_type, width=6)

        count_by_type_count = map(list, xqs.order_by('-num_results').values_list('message_type', 'num_results'))
        graph12 = XGraphCK('pie', count_by_type_count, width=6)

        # Put graphs on page
        graphpage.objs.append(XGraphRow([graph11, graph12], text_before=host_text))

    return locals()


########################################################################################################################
#
# syslog_demo 8c
#
########################################################################################################################


# noinspection PyDocstring
def syslog_demo_8c():

    # set the company and node values, ignour start/end date time for now
    company = 'BMC_1'

    # Create graphpage
    graphpage = XGraphPage()

    # Put title and some text on the page
    graphpage.text_before = 'Critical and Error Event Summary for {{ company }}\n' \
                            '==================================================\n'

    ################################################################################
    #
    # Display summary of critical and error events for all hosts for this company
    #
    ################################################################################

    qs = syslog_query(company)
    all_count = qs.count()

    # Count critical events
    critical_event_count = map(list, qs.filter(message_type='critical').
                               order_by('node__host_name').
                               values('node__host_name').
                               annotate(count=Count('node__host_name')).
                               values_list('node__host_name', 'count'))
    critical_event_count_title = '<h3>Critical Event Count by Host</h3>'
    graph31 = XGraphCK('column', 'critical_event_count',
                       width=3,
                       text_before=critical_event_count_title)
    graph32 = XGraphCK('pie', 'critical_event_count',
                       width=3,
                       text_before=critical_event_count_title)
    error_event_count = map(list, qs.filter(message_type='error').
                            order_by('node__host_name').
                            values('node__host_name').
                            annotate(count=Count('node__host_name')).
                            values_list('node__host_name', 'count'))
    error_event_count_title = '<h3>Error Event Count by Host</h3>'
    graph33 = XGraphCK('column', 'error_event_count',
                       width=3,
                       text_before=error_event_count_title)
    graph34 = XGraphCK('pie', 'error_event_count',
                       width=3,
                       text_before=error_event_count_title)
    text_before = '<h3>Company {{company}} All Hosts</h3>' \
                  '<p>Total syslog records {{all_count}}</p>'
    graphpage.objs.append(XGraphRow([graph31, graph32, graph33, graph34], text_before=text_before))

    ################################################################################
    #
    # Display summary by event type for all hosts for this company
    #
    ################################################################################

    qs = syslog_query(company)

    # count and build title
    count = qs.count()
    host_text = '<h3>Company: {}</h3>' \
                '<p>Total syslog records {}</p>' \
        .format(company, count)

    # Count by type
    xqs = qs.values('message_type').annotate(num_results=Count('id'))

    count_by_type_type = map(list, xqs.order_by('message_type').values_list('message_type', 'num_results'))
    graph21 = XGraphCK('column', count_by_type_type, width=6)

    count_by_type_count = map(list, xqs.order_by('-num_results').values_list('message_type', 'num_results'))
    graph22 = XGraphCK('pie', count_by_type_count, width=6)

    # Put graphs on page
    graphpage.objs.append(XGraphRow([graph21, graph22], text_before=host_text))

    ################################################################################
    #
    # Display summary by event type for all hosts by for this company
    #
    ################################################################################

    qs = syslog_query(company)

    # count and build title
    count = qs.count()
    host_text = '<h3>Company: {}</h3>' \
                '<p>Total syslog records {}</p>' \
        .format(company, count)

    # Count by type
    xqs = qs.values('message_type', 'node__host_name').annotate(num_results=Count('id'))

    count_by_type_type = map(list,
                             xqs.order_by('message_type').values_list('message_type', 'node__host_name', 'num_results'))
    graph41 = XGraphCK('column', count_by_type_type, width=6)

    count_by_type_count = map(list, xqs.order_by('-num_results').values_list('message_type', 'node__host_name',
                                                                             'num_results'))
    graph42 = XGraphCK('pie', count_by_type_count, width=6)

    # Put graphs on page
    graphpage.objs.append(XGraphRow([graph41, graph42], text_before=host_text))

    ################################################################################
    #
    # Display summary for each host for this company
    #
    ################################################################################

    # get the hosts for this company and put it on the page
    hosts = [n[0] for n in VNode.objects.filter(company__company_name=company).values_list('host_name')]
    hosts_text = '<h3>The company has the following hosts: ' + ', '.join(hosts) + '</h3>'
    graphpage.objs.append(XGraphRow(text_before=hosts_text))

    for host in hosts:
        # get the syslog qs for this company/node
        qs = syslog_query(company, host)

        # count and build title
        count = qs.count()
        host_text = '<h3>Company: {} Host: {}</h3>' \
                    '<p>Total syslog records {}</p>' \
            .format(company, host, count)

        # Count by type
        xqs = qs.values('message_type').annotate(num_results=Count('id'))

        count_by_type_type = map(list, xqs.order_by('message_type').values_list('message_type', 'num_results'))
        graph11 = XGraphCK('column', count_by_type_type, width=6)

        count_by_type_count = map(list, xqs.order_by('-num_results').values_list('message_type', 'num_results'))
        graph12 = XGraphCK('pie', count_by_type_count, width=6)

        # Put graphs on page
        graphpage.objs.append(XGraphRow([graph11, graph12], text_before=host_text))

    return locals()
