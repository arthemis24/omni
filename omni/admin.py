# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from threading import Thread

from django.conf import settings
from django.contrib import admin

from import_export import resources, fields

from omni.models import Refill


class RefillResource(resources.ModelResource):
    member = fields.Field(column_name='Customer')
    card_number = fields.Field(column_name='Card number')
    last_digit = fields.Field(column_name='Last 4 digits')
    amount = fields.Field(column_name='Amount')
    created_on = fields.Field(column_name='Date')

    class Meta:
        model = Refill

        fields = ('detail', 'card_number', 'CMPPCDSXAF', 'empty', 'JUMBOPAY', 'empty', 'empty', 'empty', 'CMGTP', 'CMGTP',
                  'empty', 'empty', 'empty', 'card_number', 'currency', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty',
                  'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty',
                  'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', '0020122633125001',
                  'currency', 'empty',  'empty',  'empty', 'amount', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty',
                  'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'last_digit', 'tx_description',
                  'last_digit', 'tx_description',  'last_digit', 'tx_description','empty', 'empty', 'empty', 't','1',
                  'amount' 'empty', 'empty',)
        export_order = ('detail', 'card_number', 'CMPPCDSXAF', 'empty', 'JUMBOPAY', 'empty', 'empty', 'empty', 'CMGTP', 'CMGTP',
                  'empty', 'empty', 'empty', 'card_number', 'currency', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty',
                  'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty',
                  'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', '0020122633125001',
                  'currency', 'empty',  'empty',  'empty', 'amount', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty',
                  'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'last_digit', 'tx_description',
                  'last_digit', 'tx_description',  'last_digit', 'tx_description','empty', 'empty', 'empty', 't','1',
                  'amount' 'empty', 'empty',)

    def dehydrate_created_on(refill):
        return refill.created_on.strftime('%Y-%m-%d %H:%M%S')

    def dehydrate_member(self, refill):
        return refill.member.full_name

    def dehydrate_card_number(self, refill):
        return refill.card_number

    def dehydrate_amount(self, refill):
        return refill.amount * 100

    def dehydrate_last_digit(self, refill):
        return refill.last_digit

    def dehydrate_empty(self, refill):
        return ''

    def dehydrate_tx_number(self, refill):
        return refill.last_digit

    def dehydrate_detail(self, refill):
        return 'D'

    def dehydrate_CMPPCDSXAF(self, refill):
        return 'CMPPCDSXAF'

    def dehydrate_JUMBOPAY(self, refill):
        return 'JUMBOPAY'

    def dehydrate_CMGTP(self, refill):
        return 'CMGTP'

    def dehydrate_currency(self, refill):
        return 'XAF'

    def dehydrate_0020122633125001(self, refill):
        return '0020122633125001'

    def dehydrate_tx_description(self, refill):
        description = 'Recharge carte %s' %refill.member.username
        return description


    def dehydrate_t(self, refill):
        return 'T'


    def dehydrate_1(self, refill):
        return '1'

    def dehydrate_tx_ref(self, refill):
        now = datetime.now()
        year = now.strftime("%Y")
        month = now.strftime("%m")
        day = now.strftime("%d")
        date_format = "%s%s%s" %(year, month, day)
        refill_count = Refill.objects.all().count()
        reference =  'CARTE %s%s' %(date_format, refill_count + 1)
        return reference


class RefillAdmin(admin.ModelAdmin):
    list_display = ('member', 'card_number', 'last_digit', 'amount', 'created_on')
    search_fields = ('member', 'card_number',)
    ordering = ('-id', )
    list_filter = ('created_on',)

