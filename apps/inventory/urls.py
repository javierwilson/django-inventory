from django.conf.urls import *
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy

from generic_views.views import generic_assign_remove

from photos.views import generic_photos

from models import ItemTemplate, InventoryTransaction, \
                   Inventory, Log, Location, Supplier
                   
from forms import InventoryTransactionForm, InventoryForm, \
                  ItemTemplateForm, ItemTemplateForm_view, LogForm, \
                  SupplierForm, LocationForm_view

from common.views import ExtraListView, ExtraDetailView, ExtraCreateView, ExtraUpdateView, ExtraDeleteView
from inventory.views import TemplateItemsView

from conf import settings as inventory_settings
                                

urlpatterns = patterns('inventory.views',
    url(r'^template/list/$', ExtraListView.as_view(queryset=ItemTemplate.objects.all(), extra_context=dict(title=_(u'item template'))), name='template_list'),
    url(r'^template/create/$', ExtraCreateView.as_view(form_class=ItemTemplateForm, template_name='generic_form.html', extra_context={'object_name':_(u'item template')}), name='template_create'),
    url(r'^template/(?P<pk>\d+)/update/$', ExtraUpdateView.as_view(form_class=ItemTemplateForm, queryset=ItemTemplate.objects.all(), template_name='generic_form.html', extra_context={'object_name':_(u'item template')}), name='template_update' ),
    url(r'^template/(?P<pk>\d+)/delete/$', ExtraDeleteView.as_view(), dict({'model':ItemTemplate}, success_url=reverse_lazy("template_list"), extra_context=dict(object_name=_(u'item template'), _message=_(u"Will be deleted from any user that may have it assigned and from any item group."))), name='template_delete' ),
    url(r'^template/orphans/$', ExtraListView.as_view(queryset=ItemTemplate.objects.filter(item=None), extra_context=dict(title=_('orphan templates'))), name='template_orphans_list'),
    url(r'^template/(?P<object_id>\d+)/photos/$', generic_photos, {'model':ItemTemplate, 'max_photos':inventory_settings.MAX_TEMPLATE_PHOTOS, 'extra_context':{'object_name':_(u'item template')}}, name='template_photos'), 
    url(r'^template/(?P<pk>\d+)/$', ExtraDetailView.as_view(form_class=ItemTemplateForm_view, queryset=ItemTemplate.objects.all(), extra_context={'object_name':_(u'item template'), 'sidebar_subtemplates':['generic_photos_subtemplate.html']}), name='template_view'),
    #url(r'^template/(?P<object_id>\d+)/items/$', ExtraListView.as_view(queryset=ItemTemplate.item_set.all(), template_name='generic_list.html'), name='template_items_list'),
    #url(r'^template/(?P<object_id>\d+)/items/$', 'template_items', name='template_items_list'),
    url(r'^template/(?P<object_id>\d+)/items/$', TemplateItemsView.as_view(), name='template_items_list'),
    url(r'^template/(?P<object_id>\d+)/assign/supplies$', 'template_assign_remove_supply', name='template_assign_supply'),
    url(r'^template/(?P<object_id>\d+)/assign/suppliers/$', 'template_assign_remove_suppliers', name='template_assign_suppliers'),

    url(r'^inventory/list/$', ExtraListView.as_view(queryset=Inventory.objects.all(), extra_context=dict(title=_(u'inventories'), extra_columns=[{'name':_(u'location'), 'attribute':'location'}])), name='inventory_list'),
    url(r'^inventory/create/$', ExtraCreateView.as_view(model=Inventory, template_name='generic_form.html', extra_context={'object_name':_(u'inventory')}), name='inventory_create'),
    url(r'^inventory/(?P<object_id>\d+)/$', 'inventory_view', name='inventory_view'),
    url(r'^inventory/(?P<pk>\d+)/update/$', ExtraUpdateView.as_view(form_class=InventoryForm, queryset=Inventory.objects.all(), template_name='generic_form.html', extra_context={'object_name':_(u'inventory')}), name='inventory_update'),
    url(r'^inventory/(?P<pk>\d+)/delete/$', ExtraDeleteView.as_view(model=Inventory, success_url=reverse_lazy("inventory_list"), extra_context=dict(object_name=_(u'inventory'))), name='inventory_delete'),
    #url(r'^inventory/(?P<pk>\d+)/current/$', 'inventory_current', (), 'inventory_current'),
    url(r'^inventory/(?P<object_id>\d+)/transaction/create/$', 'inventory_create_transaction', name='inventory_create_transaction'),
    url(r'^inventory/(?P<object_id>\d+)/transaction/list/$', 'inventory_list_transactions', name='inventory_list_transactions'),

    url(r'^transaction/list/$', ExtraListView.as_view(queryset=InventoryTransaction.objects.all(), extra_context=dict(title=_(u'transactions'))), name='inventory_transaction_list'),
    url(r'^transaction/create/$', ExtraCreateView.as_view(model=InventoryTransaction, template_name='generic_form.html', extra_context={'object_name':_(u'transaction')}), name='inventory_transaction_create'),
    url(r'^transaction/(?P<pk>\d+)/$', ExtraDetailView.as_view(form_class=InventoryTransactionForm, queryset=InventoryTransaction.objects.all(), extra_context={'object_name':_(u'transaction')}), name='inventory_transaction_view'),
    url(r'^transaction/(?P<pk>\d+)/update/$', ExtraUpdateView.as_view(model=InventoryTransaction, template_name='generic_form.html', extra_context={'object_name':_(u'transaction')}), name='inventory_transaction_update'),
    url(r'^transaction/(?P<pk>\d+)/delete/$', ExtraDeleteView.as_view(model=InventoryTransaction, success_url=reverse_lazy('inventory_list'), extra_context=dict(object_name=_(u'inventory transaction'))), name='inventory_transaction_delete'),

    url(r'^location/list/$', ExtraListView.as_view(queryset=Location.objects.all(), extra_context=dict(title =_(u'locations'))), name='location_list'),
    url(r'^location/create/$', ExtraCreateView.as_view(model=Location, template_name='generic_form.html'), name='location_create'),
    url(r'^location/(?P<pk>\d+)/update/$', ExtraUpdateView.as_view(model=Location, template_name='generic_form.html'), name='location_update'),
    url(r'^location/(?P<pk>\d+)/delete/$', ExtraDeleteView.as_view(), dict({'model':Location}, success_url=reverse_lazy("location_list"), extra_context=dict(object_name=_(u'locations'))), 'location_delete'),
    url(r'^location/(?P<pk>\d+)/$', ExtraDetailView.as_view(form_class=LocationForm_view, queryset=Location.objects.all()), name='location_view'),

    url(r'^supplier/(?P<pk>\d+)/$', ExtraDetailView.as_view(form_class=SupplierForm, queryset=Supplier.objects.all()), name='supplier_view'),
    url(r'^supplier/list/$', ExtraListView.as_view(queryset=Supplier.objects.all(), extra_context=dict(title=_(u'suppliers'))), name='supplier_list'),
    url(r'^supplier/create/$', ExtraCreateView.as_view(form_class=SupplierForm, template_name='generic_form.html'), name='supplier_create'),
    url(r'^supplier/(?P<pk>\d+)/update/$', ExtraUpdateView.as_view(form_class=SupplierForm, queryset=Supplier.objects.all(), template_name='generic_form.html'), name='supplier_update'),
    url(r'^supplier/(?P<pk>\d+)/delete/$', ExtraDeleteView.as_view(), dict({'model':Supplier}, success_url=reverse_lazy("supplier_list"), extra_context=dict(object_name=_(u'supplier'))), 'supplier_delete'),
    url(r'^supplier/(?P<object_id>\d+)/assign/itemtemplates/$', 'supplier_assign_remove_itemtemplates', name='supplier_assign_itemtemplates'),
    url(r'^supplier/(?P<object_id>\d+)/purchase/orders/$', 'supplier_purchase_orders', name='supplier_purchase_orders'),
    
#    url(r'^reports/items_per_person/(?P<pk>\d+)/$', 'report_items_per_person', (), 'report_items_per_person'),
)
    

