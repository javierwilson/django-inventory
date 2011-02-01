from django.utils.translation import ugettext as _
from django.template import add_to_builtins

# install default filters
add_to_builtins('report_generator.defaultfilters')
