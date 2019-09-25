# -*- coding: utf-8 -*-

__author__ = 'Roddy Mbogning'

from django.db import models
from ikwen.core.models import Model
from ikwen.accesscontrol.models import Member
from ikwen.core.constants import *


class Card(Model):
    member = models.ForeignKey(Member)
    number = models.CharField(max_length=200, null=True, blank=True)
    expired_date = models.DateField()
    is_active = models.BooleanField(default=False)


class Refill(Model):
    member = models.ForeignKey(Member)
    card_number = models.CharField(max_length=200, null=True, blank=True)
    last_digit = models.CharField(max_length=4)
    amount = models.IntegerField()
    mean = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(choices=STATUS_CHOICES, default=PENDING)

    def __unicode__(self):
        return "%s - %s" %(self.card_number, self.amount)