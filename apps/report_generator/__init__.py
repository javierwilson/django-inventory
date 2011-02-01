from django.utils.translation import ugettext_lazy as _
from django.template import add_to_builtins

from common.api import register_links, register_menu

from models import Report

# install default filters
add_to_builtins('report_generator.defaultfilters')

report_list = {'text':_(u'reports'), 'view':'report_list', 'famfam':'report_go'}
report_preview = {'text':_(u'report preview'), 'view':'report_preview', 'args':'object.id', 'famfam':'report_magnify'}
report_render = {'text':_(u'generate report'), 'view':'report_render', 'args':'object.id', 'famfam':'report_disk'}

#register_links(['item_list', 'item_view', 'item_create', 'item_orphans_list', 'item_update', 'item_delete', 'item_photos', 'item_assign_person', 'template_items_list'], [asset_create], menu_name='sidebar')
register_links(Report, [report_preview, report_render])

#register_links(['person_list', 'person_create', 'person_view', 'person_update', 'person_delete', 'person_photos', 'person_assign_item'], [person_create], menu_name='sidebar')
#register_links(Person, [person_update, person_delete, person_photos, person_assign_item])

#register_links(['group_list', 'group_view', 'group_create', 'group_update', 'group_delete'], [group_create], menu_name='sidebar')
#register_links(ItemGroup, [group_update, group_delete])

#register_links(['state_list', 'state_create', 'state_update', 'state_delete'], [state_create], menu_name='sidebar')
#register_links(State, [state_edit, state_delete])


register_menu([
    {'text':_('reports'), 'view':'report_list', 'links':[
        report_list
    ], 'famfam':'report', 'position':10},
])

