from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _



#TODO: Statistics
	# - user, parameters, execution time
	
DEFAULT_STYLE = """
@page {
    size: letter portrait;	
    margin: 1.5cm;
    margin-bottom: 2.5cm;

    @frame footer {
        -pdf-frame-content: page_footer;
        bottom: 2cm;
        margin-left: 1.5cm;
        margin-right: 1.5cm;
        height: 1cm;
    }

    @frame header { 
        -pdf-frame-content: page_header; 
        top:0cm; 
        margin-left: 1.5cm; 
        margin-right: 1.5cm; 
    } 
}

"""

class Report(models.Model):
	name = models.CharField(max_length = 128, verbose_name = _(u'name'))
	description = models.TextField(null = True, blank = True, verbose_name = _(u'description'))
	#user
	creation_datetime = models.DateTimeField(auto_now_add = True, verbose_name = _(u"creation date & time"))
	modified = models.DateTimeField(auto_now=True, verbose_name = _(u'modified'))	
	extra_tags = models.TextField(blank = True, null = True, verbose_name = _(u'extra tags'), help_text = _(u'Use this textbox to load any additional template tag libraries you wish to use, ie: {% load my_custom_filters %}.'))
	css_style = models.TextField(blank = True, null = True, verbose_name = _(u'CSS style'), default = DEFAULT_STYLE, help_text = _(u'Use only the subset of styles supported by pisa.'))
	page_header = models.TextField(blank = True, null = True, verbose_name = _(u'page header'), help_text = _(u'Element that is meant to be displayed at the beginning of every page, the element is identified with the id #page_header.'))
	page_footer = models.TextField(blank = True, null = True, verbose_name = _(u'page footer'), help_text = _(u'Element that is meant to be displayed at the end of every page, the element is identified with the id #page_footer.'))		
	model = models.ForeignKey(ContentType, verbose_name = _(u'model'))
	filter_string = models.CharField(blank = True, null = True, max_length = 128, verbose_name = _(u'filter'), help_text = _(u"Enter the filter or exclude command chain that represent the query you wish to execute, ie: filter(name__contains='Rob').exclude(last_name__='White').  Use only single quotes.  If this entry is left blank, 'objects.all()' will be used instead."))
	order_by = models.CharField(blank = True, null = True, max_length = 64, verbose_name = _(u'order by'), help_text = _(u'Unlike the filter string entry, specifying the method (order_by) is not required only the fields to order the set by.'))

	def __unicode__(self):
		return self.name

	def save(self, *args, **kwargs):
		if not self.filter_string:
			self.filter_string = "objects.all()"
		super(Report, self).save(*args, **kwargs)	
		
	class Meta:
		ordering = ('name',)
		verbose_name = _(u"report")
		verbose_name_plural = _(u"reports")	


class Parameter(models.Model):
	report = models.ForeignKey(Report, verbose_name = _(u'report'))
	name = models.CharField(max_length = 32, verbose_name = _(u'name'))
	caption = models.CharField(max_length = 32, verbose_name = _(u'caption'))
	help_text = models.TextField(null = True, blank = True, verbose_name = _(u'help text'))
	required = models.BooleanField(default = False, verbose_name = _('required?'))
	#data_type = 
	#default_value
	#argument
	#options

	def __unicode__(self):
		return self.name
		
	class Meta:
		ordering = ('name',)
		verbose_name = _(u"parameter")
		verbose_name_plural = _(u"parameters")	


#TODO: order
class Group(models.Model):
	report = models.ForeignKey(Report, verbose_name=_(u'report'))
	name = models.CharField(max_length=32, verbose_name=_(u'name'))
	#datasource = models.ForeignKey(DataSource, verbose_name = _(u'data source'))
#	model = models.ForeignKey(ContentType, verbose_name = _(u'model'))
	#OR
	#parent_datasource = models.OneToOneField('DataSource')# related_name='_unused_1')	

	filter_string = models.CharField(blank=True, null=True, max_length=128, verbose_name=_(u'filter'), help_text=_(u"Enter the filter or exclude command chain that represent the query you wish to execute, ie: filter(name__contains='Rob').exclude(last_name__='White').  Use only single quotes for strings.  If this entry is left blank, 'objects.all()' will be used instead."))
	order_by = models.CharField(blank = True, null = True, max_length = 64, verbose_name = _(u'order by'), help_text = _(u'Unlike the filter string entry, specifying the method (order_by) is not required only the fields to order the set by.'))
	group_by = models.CharField(blank = True, null = True, max_length = 128, verbose_name = _(u'group by'))
	header = models.TextField(blank = True, null = True, verbose_name = _(u'header'), help_text = _(u'Element that is displayed at the beginning of every group, the element is identified with the id #group_<group_name>_header and belongs to the class group_header.'))
	detail = models.TextField(blank = True, null = True, verbose_name = _(u'detail'), help_text = _(u'Element that is displayed as the body of every group, the element is identified with the id #group_<group_name>_detail and belongs to the class group_detail.'))
	footer = models.TextField(blank = True, null = True, verbose_name = _(u'footer'), help_text = _(u'Element that is displayed at the end of every group, the element is identified with the id #group_<group_name>_footer and belongs to the class group_footer.'))	
	parent = models.ForeignKey('self', blank = True, null = True, related_name = 'child_set', verbose_name = _(u'parent group'))
	
	def __unicode__(self):
		if not self.parent:
			return "Top group: %s%s grouped by %s" % (self.report.model, (self.report.filter_string and ".%s" % self.report.filter_string) or '', self.group_by)
		else:
			return "%s %sand grouped by %s" % (self.parent, (self.filter_string and 'filtered by %s ' % self.filter_string) or '', self.group_by)

	class Meta:
		#ordering = ('name',)
		verbose_name = _(u"group")
		verbose_name_plural = _(u"groups")	

'''
class DataSource(models.Model):
	#report = models.ForeignKey(Report, verbose_name = _(u'report'))
	group = models.ForeignKey(Group, verbose_name = _(u'group'))
	model = models.ForeignKey(ContentType, verbose_name = _(u'model'))
	filter_string = models.CharField(max_length = 128, verbose_name = _(u'filter'))
	#parameter?
	
	def __unicode__(self):
		return unicode(self.model)
		
	class Meta:
		#ordering = ('name',)
		verbose_name = _(u"data source")
		verbose_name_plural = _(u"data sources")	
'''
