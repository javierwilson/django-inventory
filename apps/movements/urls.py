from django.conf.urls import *
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy

from generic_views.views import generic_assign_remove

from models import PurchaseRequestStatus, PurchaseRequest, \
                   PurchaseRequestItem, PurchaseOrderStatus, \
                   PurchaseOrderItemStatus, PurchaseOrder, \
                   PurchaseOrderItem

from movements import purchase_request_state_filter, \
                      purchase_order_state_filter

from forms import PurchaseRequestForm, PurchaseOrderForm, PurchaseOrderItemForm
from common.views import ExtraListView, ExtraDetailView, ExtraCreateView, ExtraUpdateView, ExtraDeleteView

urlpatterns = patterns('movements.views',
    url(r'^purchase/request/state/list/$', ExtraListView.as_view(queryset=PurchaseRequestStatus.objects.all(), extra_context={'title':_(u'purchase request states')}), name='purchase_request_state_list'),
    url(r'^purchase/request/state/create/$', ExtraCreateView.as_view(model=PurchaseRequestStatus, template_name='generic_form.html', extra_context={'title':_(u'create new purchase request state')}), name='purchase_request_state_create'),
    url(r'^purchase/request/state/(?P<pk>\d+)/update/$', ExtraUpdateView.as_view(model=PurchaseRequestStatus, template_name='generic_form.html'), name='purchase_request_state_update'),
    url(r'^purchase/request/state/(?P<object_id>\d+)/delete/$', ExtraDeleteView.as_view(model=PurchaseRequestStatus, success_url=reverse_lazy("purchase_request_state_list"), extra_context=dict(object_name=_(u'purchase request state'))), name='purchase_request_state_delete'),

    url(r'^purchase/request/list/$', ExtraListView.as_view(queryset=PurchaseRequest.objects.all(), list_filters=[purchase_request_state_filter], extra_context=dict(title =_(u'purchase requests'), extra_columns = [{'name':_(u'Active'), 'attribute':lambda x: _(u'Open') if x.active == True else _(u'Closed')}])), name='purchase_request_list'),
    url(r'^purchase/request/(?P<object_id>\d+)/$', 'purchase_request_view', (), 'purchase_request_view'),
    url(r'^purchase/request/create/$', ExtraCreateView.as_view(form_class=PurchaseRequestForm, template_name='generic_form.html', extra_context={'title':_(u'create new purchase request')}), name='purchase_request_create'),
    url(r'^purchase/request/(?P<pk>\d+)/update/$', ExtraUpdateView.as_view(form_class=PurchaseRequestForm, queryset=PurchaseRequest.objects.all(), template_name='generic_form.html'), name='purchase_request_update'),
    url(r'^purchase/request/(?P<object_id>\d+)/delete/$', ExtraDeleteView.as_view(model=PurchaseRequest, success_url=reverse_lazy("purchase_request_list"), extra_context=dict(object_name=_(u'purchase request'))), name='purchase_request_delete'),
    url(r'^purchase/request/(?P<object_id>\d+)/close/$', 'purchase_request_close', (), 'purchase_request_close'),
    url(r'^purchase/request/(?P<object_id>\d+)/open/$', 'purchase_request_open', (), 'purchase_request_open'),
    url(r'^purchase/request/(?P<object_id>\d+)/purchase_order_wizard/$', 'purchase_order_wizard', (), 'purchase_order_wizard'),

    url(r'^purchase/request/(?P<object_id>\d+)/add_item/$', 'purchase_request_item_create', (), 'purchase_request_item_create'),
    url(r'^purchase/request/item/(?P<pk>\d+)/update/$', ExtraUpdateView.as_view(model=PurchaseRequestItem, template_name='generic_form.html'), name='purchase_request_item_update'),
    url(r'^purchase/request/item/(?P<object_id>\d+)/delete/$', ExtraDeleteView.as_view(model=PurchaseRequestItem, success_url=reverse_lazy("purchase_request_list"), extra_context=dict(object_name=_(u'purchase request item'))), name='purchase_request_item_delete'),

    url(r'^purchase/order/state/list/$', ExtraListView.as_view(queryset=PurchaseOrderStatus.objects.all(), extra_context=dict(title =_(u'purchase order states'))), name='purchase_order_state_list'),
    url(r'^purchase/order/state/create/$', ExtraCreateView.as_view(model=PurchaseOrderStatus, template_name='generic_form.html', extra_context={'title':_(u'create new purchase order state')}), name='purchase_order_state_create'),
    url(r'^purchase/order/state/(?P<pk>\d+)/update/$', ExtraUpdateView.as_view(model=PurchaseOrderStatus, template_name='generic_form.html'), name='purchase_order_state_update'),
    url(r'^purchase/order/state/(?P<pk>\d+)/delete/$', ExtraDeleteView.as_view(model=PurchaseOrderStatus, success_url=reverse_lazy("purchase_order_state_list"), extra_context=dict(object_name=_(u'purchase order status'))), name='purchase_order_state_delete'),

    url(r'^purchase/order/list/$', ExtraListView.as_view(queryset=PurchaseOrder.objects.all(), list_filters=[purchase_order_state_filter], extra_context=dict(title =_(u'purchase orders'), extra_columns = [{'name':_(u'Active'), 'attribute':lambda x: _(u'Open') if x.active == True else _(u'Closed')}])), name='purchase_order_list'),
    url(r'^purchase/order/(?P<object_id>\d+)/$', 'purchase_order_view', (), 'purchase_order_view'),
    url(r'^purchase/order/create/$', ExtraCreateView.as_view(form_class=PurchaseOrderForm, template_name='generic_form.html', extra_context={'title':_(u'create new purchase order')}), name='purchase_order_create'),
    url(r'^purchase/order/(?P<object_id>\d+)/update/$', ExtraUpdateView.as_view(form_class=PurchaseOrderForm, template_name='generic_form.html'), name='purchase_order_update'),
    url(r'^purchase/order/(?P<object_id>\d+)/delete/$', ExtraDeleteView.as_view(model=PurchaseOrder, success_url=reverse_lazy("purchase_order_list"), extra_context=dict(object_name=_(u'purchase order'))), name='purchase_order_delete'),
    url(r'^purchase/order/(?P<object_id>\d+)/close/$', 'purchase_order_close', (), 'purchase_order_close'),
    url(r'^purchase/order/(?P<object_id>\d+)/open/$', 'purchase_order_open', (), 'purchase_order_open'),
    url(r'^purchase/order/(?P<object_id>\d+)/add_item/$', 'purchase_order_item_create', (), 'purchase_order_item_create'),
    url(r'^purchase/order/(?P<object_id>\d+)/transfer/$', 'purchase_order_transfer', (), 'purchase_order_transfer'),

    url(r'^purchase/order/item/state/list/$', ExtraListView.as_view(queryset=PurchaseOrderItemStatus.objects.all(), extra_context={'title':_(u'purchase order item states')}), name='purchase_order_item_state_list'),
    url(r'^purchase/order/item/state/create/$', ExtraCreateView.as_view(model=PurchaseOrderItemStatus, template_name='generic_form.html', extra_context={'title':_(u'create new purchase order item state')}), name='purchase_order_item_state_create'),
    url(r'^purchase/order/item/state/(?P<pk>\d+)/update/$', ExtraUpdateView.as_view(model=PurchaseOrderItemStatus, template_name='generic_form.html'), name='purchase_order_item_state_update'),
    url(r'^purchase/order/item/state/(?P<object_id>\d+)/delete/$', ExtraDeleteView.as_view(model=PurchaseOrderItemStatus, success_url=reverse_lazy("purchase_order_item_state_list"), extra_context=dict(object_name=_(u'purchase order item status'))), name='purchase_order_item_state_delete'),

    url(r'^purchase/order/item/(?P<pk>\d+)/update/$', ExtraUpdateView.as_view(form_class=PurchaseOrderItemForm, template_name='generic_form.html'), name='purchase_order_item_update'),
    url(r'^purchase/order/item/(?P<object_id>\d+)/delete/$', ExtraDeleteView.as_view(model=PurchaseOrderItem, success_url=reverse_lazy("purchase_order_list"), extra_context=dict(object_name=_(u'purchase order item'))), name='purchase_order_item_delete'),
    url(r'^purchase/order/item/(?P<object_id>\d+)/close/$', 'purchase_order_item_close', (), 'purchase_order_item_close'),
    url(r'^purchase/order/item/(?P<object_id>\d+)/transfer/$', 'purchase_order_item_transfer', (), 'purchase_order_item_transfer'),

)
    

