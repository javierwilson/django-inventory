from django.conf.urls.defaults import *
from django.utils.translation import ugettext_lazy as _


from generic_views.views import generic_list, generic_detail


from models import Report
from forms import ReportForm_view


urlpatterns = patterns('report_generator.views',
    url(r'^report/list/$', generic_list, dict({'queryset':Report.objects.all()}, extra_context=dict(title =_(u'reports'))), 'report_list'),
    url(r'^report/(?P<object_id>\d+)/$', generic_detail, {'form_class':ReportForm_view, 'queryset':Report.objects.all()}, 'report_view'),
    url(r'^report/(?P<report_id>\d+)/render/$', 'report_render', ({'mode':'pdf'}), 'report_render'),
    url(r'^report/(?P<report_id>\d+)/preview/$', 'report_render', ({'mode':'html'}), 'report_preview'),
    url(r'^report/(?P<report_id>\d+)/debug/$', 'report_render', ({'mode':'raw'}), 'report_debug'),

    url(r'^report/(?P<report_id>\d+)/preview/for/(?P<app_label>[\w\-]+)/(?P<model>[\w\-]+)/(?P<pk>\d+)/$', 'report_render', ({'mode':'html'}), 'report_preview_for_object'),    
    url(r'^report/(?P<report_id>\d+)/render/for/(?P<app_label>[\w\-]+)/(?P<model>[\w\-]+)/(?P<pk>\d+)/$', 'report_render', ({'mode':'pdf'}), 'report_render_for_object'),    
    url(r'^report/(?P<report_id>\d+)/debug/for/(?P<app_label>[\w\-]+)/(?P<model>[\w\-]+)/(?P<pk>\d+)/$', 'report_render', ({'mode':'raw'}), 'report_raw_for_object'),    
)
