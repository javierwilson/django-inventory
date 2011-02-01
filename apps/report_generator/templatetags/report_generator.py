#from django.template import Node, Variable
from django.template import TemplateSyntaxError, Library, VariableDoesNotExist
from django.template.defaultfilters import stringfilter
from django.template.defaultfilters import date as datefilter
#from django.conf import settings

register = Library()

@register.filter
def eval_qs_filter(qs, extra_filters):
	result = eval("qs.%s" % extra_filters, { 'qs' :  qs })
	return result
	
@register.filter
def eval_sorting(qs, fields):
	result = eval("qs.order_by('%s')" % fields, { 'qs' :  qs })
	return result
