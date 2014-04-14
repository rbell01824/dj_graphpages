#!/usr/bin/env python

"""

11/18/13 - Initial creation

"""

from __future__ import unicode_literals
import logging
log = logging.getLogger(__name__)

__author__ = 'rbell01824'
__date__ = '11/18/13'
__copyright__ = "Copyright 2013, Richard Bell"
__credits__ = ["rbell01824"]
__license__ = "All rights reserved"
__version__ = "0.1"
__maintainer__ = "rbell01824"
__email__ = "rbell01824@gmail.com"
__status__ = "dev"

from django.db import models


class CIA(models.Model):
    """
    cia world fact book
    """
    country_code = models.CharField(max_length=2, primary_key=True)
    name = models.CharField(max_length=50)
    total_area = models.FloatField()
    land_area = models.FloatField()
    water_area = models.FloatField()
    coastline = models.FloatField()
    total_border = models.FloatField()
    population = models.FloatField()
    p_young = models.FloatField()
    p_adult = models.FloatField()
    p_old = models.FloatField()
    p_growth = models.FloatField()
    labor_force = models.FloatField()
    phone_mobiles = models.FloatField()
    phone_mainlines = models.FloatField()
    internet_users = models.FloatField()
    isps = models.FloatField()
    birth_rate = models.FloatField()
    death_rate = models.FloatField()

    class Meta:
        verbose_name = 'CIA World Factbook'
        verbose_name_plural = 'CIA World Factbook'

    def __unicode__(self):
        return u'{}'.format(self.name)


class Countries(models.Model):
    """
    world countries
    """
    id = models.IntegerField(primary_key=True)
    a2 = models.CharField(max_length=2)
    a3 = models.CharField(max_length=2)
    num = models.IntegerField()
    country_name = models.CharField(max_length=50)
    country_size = models.IntegerField()
    population = models.IntegerField()
    life_expectancy = models.FloatField()
    infant_mortality = models.FloatField()

    class Meta:
        verbose_name = 'Countries'
        verbose_name_plural = 'Countries'

    def __unicode__(self):
        return u'{}'.format(self.country_name)


class Company(models.Model):
    company_name = models.CharField(max_length=50,  # the name of the company
                                    blank=False,
                                    help_text='Enter company name',
                                    unique=True,
                                    verbose_name='Company name')

    #noinspection PyClassicStyleClass
    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'

    def __unicode__(self):
        return unicode(self.company_name)


class Node(models.Model):
    company = models.ForeignKey(Company,            # company who has this node
                                #help_text="Select company for this node",
                                # limit_choices_to={'company_name__in': ['TestCo', 'TestCo_1']},
                                verbose_name="Company")
    node_ip = models.GenericIPAddressField(blank=True,              # node ip address
                                           null=True,
                                           # default='0.0.0.0',
                                           #help_text='IP address for this node',
                                           verbose_name='Node IP address')
    host_name = models.CharField(max_length=50,                     # host name
                                 blank=True,
                                 default='',
                                 #help_text='Host name',
                                 unique=False,
                                 verbose_name='Host name')

    #noinspection PyClassicStyleClass
    class Meta:
        verbose_name = 'Node'
        verbose_name_plural = 'Nodes'

    def __unicode__(self):
        return unicode(u"{} {}:{}".format(self.company.company_name,
                                          self.host_name, self.node_ip))


class Syslog(models.Model):
    """
    Syslog data
    """
    node = models.ForeignKey(Node,
                             null=True,
                             verbose_name='Node',
                             help_text='The node for this syslog entry')
    time = models.DateTimeField()
    text = models.CharField(max_length=128)
    type = models.CharField(max_length=50)
    error = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Syslog'
        verbose_name_plural = 'Syslog'

    def __unicode__(self):
        return u'{}:{}:{}:{}:{}'.format(self.node, self.time, self.text, self.type, self.error)

########################################################################################################################

from django.db.models import Q


def syslog_query(company=None, node=None, start_time=None, end_time=None):
    """
    Method to build a syslog query set of records in the specified company(s) and node(s).
    :param company: A company
    :param node: A node
    :param start_time: start time for syslog records
    :param end_time: end time for syslog records
    """

    # Company.objects.all()                 qs of Company objects
    # Node.objects.all()                    qs of Node objects
    # Syslog.objects.all()                  qs for syslog objects
    #
    # valuesqs of host_names for TestCo_1
    # Node.objects.filter(company__company_name='TestCo_1').values('host_name').distinct()
    #
    # valuesqs of node pks for all nodes with syslog records
    # Syslog.objects.all().order_by('node').values('node').distinct()
    #
    # values qs of pk(s) for nodes for TestCo1
    # Node.objects.filter(company__company_name='TestCo_1').values('pk').distinct()
    #
    # qs of syslog objects for TestCo_1
    # Syslog.objects.filter(node__company__company_name='TestCo_1')
    #
    # qs of syslog objects for TestCo_1 host_name A0040CnBEPC1
    # Syslog.objects.filter(node__company__company_name='TestCo_1', node__host_name='A0040CnBEPC1')
    #

    # make sure company and node are objects
    if isinstance(company, basestring):
        company = Company.objects.get(company_name=company)
    if company and isinstance(node, basestring):
        node = Node.objects.get(company=company, host_name=node)

    if node:                    # if we have a node, use it to subset the syslog records
        qs = Syslog.objects.filter(node=node)
    elif company:               # if we have a company, use it to subset the syslog records
        qs = Syslog.ojbects.filter(node__company=company)
    else:                       # work with all companies, all nodes
        qs = Syslog.objects.all()
    if start_time:
        qs = qs.filter(time__gte=start_time)
    if end_time:
        qs = qs.filter(time__lte=end_time)
    return qs
