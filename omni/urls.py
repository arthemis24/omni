from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.contrib.auth.decorators import permission_required,login_required

from omni.views import RefillCard, RefillList, start_refill_process, refill_do_checkout

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^refill$',  login_required(RefillCard.as_view()), name='refill'),
    url(r'^refillList/$', permission_required('omni.ik_omni_admin')(RefillList.as_view()), name='refill_list'),
    url(r'^start_refill_process/$', start_refill_process, name='start_refill_process'),
    url(r'^confirm_checkout$', refill_do_checkout, name='confirm_checkout'),
)
