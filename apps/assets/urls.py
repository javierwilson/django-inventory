from django.conf.urls import *
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy

from common.views import ExtraListView, ExtraDetailView, ExtraCreateView, ExtraUpdateView, ExtraDeleteView
from generic_views.views import generic_assign_remove

from photos.views import generic_photos

from inventory import location_filter

from assets import state_filter
from models import Item, ItemGroup, Person, State
from forms import ItemForm, ItemForm_view, ItemGroupForm, ItemGroupForm_view, PersonForm, PersonForm_view
from conf import settings as asset_settings                             

                                
urlpatterns = patterns('assets.views',
    url(r'^person/(?P<object_id>\d+)/photos/$', generic_photos, {'model':Person, 'max_photos':asset_settings.MAX_PERSON_PHOTOS, 'extra_context':{'object_name':_(u'person')}}, 'person_photos'), 
    url(r'^person/(?P<pk>\d+)/$', ExtraDetailView.as_view(form_class=PersonForm_view, queryset=Person.objects.all(), extra_context={'sidebar_subtemplates':['generic_photos_subtemplate.html']}), name='person_view'),
    url(r'^person/list/$', ExtraListView.as_view(queryset=Person.objects.all(), list_filters=[location_filter], extra_context={'title':_(u'people')}), name='person_list'),
    url(r'^person/create/$', ExtraCreateView.as_view(form_class=PersonForm, template_name='generic_form.html'), name='person_create'),
    url(r'^person/(?P<pk>\d+)/update/$', ExtraUpdateView.as_view(form_class=PersonForm, template_name='generic_form.html'), name='person_update'),
    url(r'^person/(?P<pk>\d+)/delete/$', ExtraDeleteView.as_view(model=Person, post_delete_redirect='person_list', extra_context={'object_name':_(u'person')}), name='person_delete'),
    url(r'^person/(?P<pk>\d+)/assign/$', 'person_assign_remove_item', (), 'person_assign_item'),

    url(r'^asset/create/$', ExtraCreateView.as_view(form_class=ItemForm, template_name='generic_form.html'), name='item_create'),
    url(r'^asset/(?P<pk>\d+)/update/$', ExtraUpdateView.as_view(form_class=ItemForm, queryset=Item.objects.all(), template_name='generic_form.html', extra_context={'object_name':_(u'asset')}), name='item_update'),
    url(r'^asset/(?P<pk>\d+)/delete/$', ExtraDeleteView.as_view(model=Item, success_url=reverse_lazy("item_list"), extra_context={'object_name':_(u'asset')}), name='item_delete'),
    url(r'^asset/(?P<object_id>\d+)/assign/$', 'item_assign_remove_person', (), name='item_assign_person'),
    url(r'^asset/orphans/$', ExtraListView.as_view(queryset=Item.objects.filter(person=None), list_filters=[location_filter], extra_context=dict(title=_(u'orphan assets'))), name='item_orphans_list'),
    url(r'^asset/list/$', ExtraListView.as_view(queryset=Item.objects.all(), list_filters=[location_filter, state_filter], extra_context=dict(title=_(u'assets'))), name='item_list'),
    url(r'^asset/(?P<pk>\d+)/$', ExtraDetailView.as_view(form_class=ItemForm_view, queryset=Item.objects.all(), extra_context={'object_name':_(u'asset'), 'sidebar_subtemplates':['generic_photos_subtemplate.html', 'state_subtemplate.html']}, extra_fields=[{'field':'get_owners', 'label':_(u'Assigned to:')}]), name='item_view'),
    url(r'^asset/(?P<object_id>\d+)/photos/$', generic_photos, {'model':Item, 'max_photos':asset_settings.MAX_ASSET_PHOTOS, 'extra_context':{'object_name':_(u'asset')}}, 'item_photos'), 
    url(r'^asset/(?P<object_id>\d+)/state/(?P<state_id>\d+)/set/$', 'item_setstate', name='item_setstate'),
    url(r'^asset/(?P<object_id>\d+)/state/(?P<state_id>\d+)/unset$', 'item_remove_state', name='item_remove_state'),

    url(r'^group/list/$', ExtraListView.as_view(queryset=ItemGroup.objects.all(), extra_context=dict(title=_(u'item groups'))), name='group_list'),
    url(r'^group/create/$', ExtraCreateView.as_view(form_class=ItemGroupForm, template_name='generic_form.html'), name='group_create'),
    url(r'^group/(?P<pk>\d+)/$', ExtraDetailView.as_view(form_class=ItemGroupForm_view, queryset=ItemGroup.objects.all()), name='group_view'),
    url(r'^group/(?P<object_id>\d+)/update/$', 'group_assign_remove_item', name='group_update'),
    url(r'^group/(?P<object_id>\d+)/delete/$', ExtraDeleteView.as_view(model=ItemGroup, success_url=reverse_lazy("group_list"), extra_context=dict(object_name=_(u'item group'))), name='group_delete'),

    url(r'^state/list/$', ExtraListView.as_view(queryset=State.objects.all(), extra_context=dict(title =_(u'states'))), name='state_list'),
    url(r'^state/create/$', ExtraCreateView.as_view(model=State, template_name='generic_form.html', extra_context={'title':'create asset state'}), name='state_create'),
    url(r'^state/(?P<pk>\d+)/update/$', ExtraUpdateView.as_view(model=State, template_name='generic_form.html'), name='state_update'),
    url(r'^state/(?P<pk>\d+)/delete/$', ExtraDeleteView.as_view(model=State, success_url=reverse_lazy("state_list"), extra_context=dict(object_name=_(u'states'))), name='state_delete'),
)
    

