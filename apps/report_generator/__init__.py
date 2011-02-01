from django.utils.translation import ugettext as _
#from django.conf import settings
#from module_manager.api import register_smart_module
from django.template import add_to_builtins

#register_smart_module(name='report_generator', title=_(u"Report generator"),
#                      register_urls=True, required_modules=['tinymce'])

# install default filters
add_to_builtins('report_generator.defaultfilters')
