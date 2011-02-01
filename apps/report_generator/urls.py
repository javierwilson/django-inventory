from django.conf.urls.defaults import *

urlpatterns = patterns('report_generator.views',
    url(r'report/(?P<report_id>\d+)/$', 'report_view', (), 'report_view'),
)
