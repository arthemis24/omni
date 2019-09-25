# coding=utf-8
import json
import datetime
import csv
from django.views.generic import TemplateView
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from ikwen.core.views import HybridListView
from ikwen.core.utils import get_service_instance
from ikwen.billing.mtnmomo.views import MTN_MOMO
from django.contrib import messages
from django.utils.translation import gettext as _

from omni.forms import RefillForm
from omni.models import Refill
from omni.admin import RefillResource
from ikwen.core.constants import *

import logging


logger = logging.getLogger('ikwen')


class RefillCard(TemplateView):
    template_name = 'omni/refill.html'

    def get_context_data(self, **kwargs):
        context = super(RefillCard, self).get_context_data(**kwargs)
        member = self.request.user
        context['refill_list'] = Refill.objects.filter(member=member, status=CONFIRMED).order_by('-id') if member.is_authenticated() else None
        return context

    def post(self, request, *args, **kwargs):
        try:
            product_id = request.POST.get('product_id')
            refill = Refill.objects.get(pk=product_id)
        except Refill.DoesNotExist:
            return HttpResponseRedirect(reverse('omni'))
        else:
            refill.status = CONFIRMED
            refill.save()
            return HttpResponseRedirect(reverse('home'))


class RefillList(HybridListView):
    queryset = Refill.objects.filter(status=CONFIRMED)
    context_object_name = 'refills'
    search_field = ('card_number, member',)
    list_filter = (('created_on', _("Date")), )
    template_name = 'omni/refill_list.html'
    html_results_template_name = 'omni/refill_list_results.html'
    export_resource = RefillResource
    page_size = 50

    def export(self, queryset):
        i = 1
        total = 0
        now = datetime.datetime.now()
        dt = now.strftime('%Y%m%d_%H%M%S')

        year = now.strftime("%Y")
        month = now.strftime("%m")
        day = now.strftime("%d")
        date_format = "%s%s%s" % (year, month, day)
        filename = 'recharge_%s.csv' % dt
        f = open(filename, 'wb')

        writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerow(["H", "JUMBOPAY", "PAYRL", '', '', '', "RECHARGE DU %s" % now, "RECHARGE CARTES"])
        for refill in queryset:
            description = 'Recharge carte %s' % refill.member.username
            reference = 'CARTE %s%s' % (date_format, i)
            i += 1
            total += int(refill.amount)
            writer.writerow(['D', reference, 'CMPPCDSXAF', '', 'JUMBOPAY', '', '', '', '', '', '', '', '',
                             refill.card_number, 'XAF', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                             '', '', '', '', '', '', '', '', '', '', '', '0020122633125001', 'XAF', '', '', '',
                             refill.amount * 100, '', '', '', '', '', '', '', '', '', '', '', '', '', refill.last_digit,
                             description, refill.last_digit, description, refill.last_digit, description, '', '', ''])

        writer.writerow(['T', '1', total * 100, '', ''])
        f.close()

        f = open(filename, 'r')
        response = HttpResponse(f, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        return response


@login_required
def start_refill_process(request, *args, **kwargs):
    member = request.user
    if not member.is_authenticated():
        return HttpResponseRedirect(reverse('ikwen:sign_in'))
    card_number = request.GET.get('card_number')
    amount = request.GET.get('amount')
    last_digit = request.GET.get('last_digit')
    if not card_number or not amount or not last_digit:
        response = {
            'Error': "One or more fields need to be provided"
        }
        return HttpResponse(json.dumps(response))
    refill = Refill(card_number=card_number, last_digit=last_digit, amount=amount, member=member)
    refill.save()
    response = {
        'refill_id': refill.id
    }
    return HttpResponse(json.dumps(response))


def refill_set_checkout(request, *args, **kwargs):
    service = get_service_instance()
    member = request.user
    refill_id = request.POST.get('product_id')
    refill = Refill.objects.get(pk=refill_id)
    request.session['amount'] = refill.amount
    request.session['model_name'] = 'billing.Donation'
    request.session['object_id'] = refill.id

    mean = request.GET.get('mean', MTN_MOMO)
    request.session['mean'] = mean
    request.session['notif_url'] = service.url # Orange Money only
    request.session['cancel_url'] = service.url + reverse('home') # Orange Money only
    request.session['return_url'] = service.url + reverse('omni:refill')


def refill_do_checkout(request, *args, **kwargs):
    refill_id = request.session['object_id']
    mean = request.session['mean']
    refill = Refill.objects.get(pk=refill_id)
    refill.status = CONFIRMED
    refill.mean = mean
    refill.save()

    service = get_service_instance()
    # config = service.config
    # if member.email:
    #     subject, message, sms_text = get_payment_confirmation_message(payment, member)
    #     html_content = get_mail_content(subject, message, template_name='billing/mails/notice.html')
    #     sender = '%s <no-reply@%s>' % (config.company_name, service.domain)
    #     msg = EmailMessage(subject, html_content, sender, [member.email])
    #     msg.content_subtype = "html"
    #     Thread(target=lambda m: m.send(), args=(msg,)).start()
    messages.success(request, _("Nous avons bien reçu votre paiement, votre carte sera rechargée dans un maximum de 24h."))
    return HttpResponseRedirect(request.session['return_url'])
