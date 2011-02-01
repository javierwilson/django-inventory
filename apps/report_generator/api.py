import re
import htmlentitydefs
import types
import os
import sys
#import cStringIO as StringIO
from cStringIO import StringIO

from django.http import HttpResponse, Http404, HttpResponseServerError
from django.shortcuts import HttpResponseRedirect, redirect
from django.template import Template, Context, RequestContext
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.conf import settings
from django.utils.translation import ugettext as _


#from django.views.debug import ExceptionReporter
from reporter import ExceptionReporter
    
try:
    import reportlab
except ImportError:
    raise ImportError, 'reportlab is not installed'

try:
    import html5lib
except ImportError:
    raise ImportError, 'html5lib is not installed'

try:
    import ho.pisa as pisa
except ImportError:
    raise ImportError, 'python-pisa (xhtmltopdf) is not installed'

from models import Report


def report_error(request, message):
    return HttpResponse(message)


#October 28, 2006 | Fredrik Lundh
#http://effbot.org/zone/re-sub.htm#unescape-html
def unescape(text):
    """Removes HTML or XML character references and entities from a text string.
    @param text The HTML (or XML) source text.
    @return The plain text, as a Unicode string, if necessary.
    """

    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)


def fetch_resources(uri, rel):
    path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ''))
    return path

def render_template(request, template_src, context_dict):
    context = Context(context_dict)

    try:
        template = Template(template_src)
        content = template.render(context)#, context_instance=RequestContext(request))
    except:
        reporter = ExceptionReporter(request, *sys.exc_info())
        content = reporter.get_traceback_html(strip_frames=4,
                                            template_context=context)
    
    return content
    

def render_to_pdf(request, template_src, context_dict):
    content = render_template(request, template_src, context_dict)
        #content = reporter.get_traceback_html()#template_context=context)

        #return HttpResponseServerError(content, mimetype='text/html')
        #return HttpResponse(content, mimetype='text/html')
    #    html=content
                            
    result = StringIO()
    pdf = pisa.pisaDocument(StringIO(content.encode("UTF-8")), result, link_callback = fetch_resources)

    if pdf.err:
        return HttpResponse(_(u'pdf error: %s' % pdf.err))
        #, <pre>%s</pre>' % escape(content))
    else:
        return HttpResponse(result.getvalue(), mimetype='application/pdf')


def render_to_response(request, template_src, context_dict):
    content = render_template(request, template_src, context_dict)
    return HttpResponse(content)


def return_attrib(obj, attrib, arguments=None):
    try:
        result = reduce(getattr, attrib.split("."), obj)
        if isinstance(result, types.MethodType):
            if arguments:
                return result(**arguments)
            else:
                return result()
        else:
            return result
    except Exception, err:
        if settings.DEBUG:
            return "Filter error: %s; %s" % (attrib, err)
        else:
            pass


def append(indent, text):
    return "%s%s\n\n" % (indent * '\t', text)


def render_group(group):
    template = ''
    qs_transformations = []
    list_sort_string = None
    
    #if group.filter_string:
    #    qs_transformations.append('eval_qs_filter:"%s"' % group.filter_string)
        
    #if group.order_by:
    #    qs_transformations.append('eval_sorting:"%s"' % group.order_by)
    #    list_sort_elements = []
    #    for field in group.order_by.split(','):
    #        if field.startswith('-'):
    #            list_sort_elements.append('dictsortreversed:"%s"' % field.lstrip('-'))
    #        else:
    #            list_sort_elements.append('dictsort:"%s"' % field)
    #
    #    list_sort_string = "|".join(list_sort_elements)
            
    #qs_transformations_string = "|".join(qs_transformations)

    if group.group_by:
        if group.group_by.startswith('-'):
            dictsort = 'dictsort:"%s"' % group.group_by.lstrip('-')
        else:
            dictsort = "dictsortreversed:'%s'" % group.group_by
        #template += append(4, '{%% regroup data_source|%(qs_transformations)s%(dictsort)s by %(group_by)s as group_list %%}' % ( { 'dictsort' : dictsort, 'group_by' : group.group_by.lstrip('-'), 'qs_transformations' : qs_transformations_string and qs_transformations_string + "|" }))
        template += append(4, '{%% regroup data_source|%(dictsort)s by %(group_by)s as group_list %%}' % ( { 'dictsort' : dictsort, 'group_by' : group.group_by.lstrip('-') }))

        template += append(4, '{% for group in group_list %}')
        template += append(4, '{% with group.grouper as group_title %}')
        template += append(4, '<div class="group_header" id="group_%s_header">%s</div>' % (group.name, unescape(group.header)))
        template += append(5, '{%% for instance in group.list|%s%s %%}' % (dictsort, "|" + list_sort_string if list_sort_string else ''))#( group.group_by and ("|dictsort:'%s'" % group.group_by) or '' ))
        template += append(4, '<div class="group_detail" id="group_%s_detail">' % group.name)
    else:
        template += append(4, '<div class="group_header" id="group_%s_header">%s</div>' % (group.name, unescape(group.header)))
        template += append(4, '<div class="group_detail" id="group_%s_detail">' % group.name)
#        template += append(5, "{%% for instance in data_source%(qs_transformations)s %%}" % ({'qs_transformations':qs_transformations_string and "|" + qs_transformations_string or ''}))
        template += append(5, "{% for instance in data_source %}")

    template += append(6, '<span class="group_detail" id="group_%s_detail">%s</span>' % (group.name, unescape(group.detail)))

    for child_group in group.child_set.all():
        template += render_group(child_group)

    if group.group_by:
        template += append(4, "</div>")
        template += append(5, '{% endfor %}')
        template += append(4, '{% endwith %}')
        template += append(4, '{% endfor %}')
    else:
        template += append(5, "{% endfor %}")
        template += append(4, "</div>")
    
    template += append(4, '<div class="group_footer" id="group_%s_footer">%s</div>' % (group.name, unescape(group.footer)))

    return template


from assets.models import Person

def generate_report(request, report, queryset=None, mode='pdf'):
    #mode = request.GET.get('mode', 'pdf')
    template = ''

    template += append(0, report.extra_tags or '')
    template += append(0, '{% load report_generator %}')
    template += append(0, '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"')
    template += append(0, '"http://www.w3.org/TR/html4/loose.dtd">')

    template += append(1, '<html>')
    template += append(2, '<meta http-equiv="content-type" content="text/html; charset=utf-8" />')
    
    template += append(2, '<head>')

    template += append(3, '<style>')

    template += append(2, report.css_style or '')	
    template += append(3, '</style>')	

    template += append(2, '</head>')

    template += append(2, '<body>')
    
    
    template += append(3, "<div id='page_header'>%s</div>" % unescape(report.page_header))

    for group in report.group_set.filter(parent=None):
        template += render_group(group)

    template += append(3, "<div id='page_footer'>%s</div>" % unescape(report.page_footer))

    template += append(2, '</body>')
    template += append(1, '</html>')

    try:
        if not queryset:
            queryset = eval(report.queryset, {'model':report.model.model_class()})
    except Exception, err:
        return report_error(request, err)
    
    context = {'data_source':queryset}
    #context = {'data_source':Person.objects.all()}#report.queryset}
    
    if mode == 'pdf':
        return render_to_pdf(request, template, context)
    elif mode == 'html':
        return render_to_response(request, template, context)
    elif mode == 'raw':
        return HttpResponse(template)
    else:
        return HttpResponse(_(u'Invalid display mode'))
