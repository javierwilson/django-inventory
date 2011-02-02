from django.utils.translation import ugettext_lazy as _
from django.template import add_to_builtins

from common.api import register_links, register_menu

from models import Report, ModelReportRelationship

# install default filters
add_to_builtins('report_generator.defaultfilters')

report_list = {'text':_(u'user reports'), 'view':'report_list', 'famfam':'report_go'}
report_preview = {'text':_(u'preview'), 'view':'report_preview', 'args':'object.id', 'famfam':'report_magnify'}
report_render = {'text':_(u'generate'), 'view':'report_render', 'args':'object.id', 'famfam':'report_disk'}
report_debug = {'text':_(u'debug'), 'view':'report_debug', 'args':'object.id', 'famfam':'report_link'}

register_links(Report, [report_preview, report_render, report_debug])

register_menu([
    {'text':_('reports'), 'view':'report_list', 'links':[
        report_list
    ], 'famfam':'report', 'position':6},
])


for relationship in ModelReportRelationship.objects.all():
    register_links(relationship.model.model_class(), [
        {
            'text':relationship.report,
            'view':'report_preview_for_object', 'args':{
                'report_id':relationship.report.id,
                'app_label':'"%s"' % relationship.model.app_label,
                'model':'"%s"' % relationship.model.model,
                'pk':'object.id',
            }, 'famfam':'report_magnify'
        }
    ], menu_name='reports')
