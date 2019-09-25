# -*- coding: utf-8 -*-

__author__ = 'Optimum Roddy'

from django import forms


class RefillForm(forms.Form):
    card_number = forms.CharField(max_length=100)
    last_digit = forms.CharField(max_length=4)
    amount = forms.IntegerField()
