from django.conf.urls.defaults import *
#from django.utils.translation import ugettext as _
#from utils import smart_modules

urlpatterns = patterns('report_generator.views',
	url(r'report/(?P<report_id>\d+)/$', 'report_view', (), 'report_view'),
#	#url(r'utils/render_module_icon/(?P<module_name>[\w\-]+)/$', 'render_module_icon', (), 'render_module_icon'),
#	url(r'utils/render_module_icon/(?P<module_name>[a-zA-Z0-9_.-]+)/$', 'render_module_icon', (), 'render_module_icon'),
)
