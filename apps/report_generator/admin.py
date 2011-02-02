from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.db import models
from tinymce.widgets import TinyMCE

from models import Report, Group, ModelReportRelationship#, Parameter


class GroupAdminForm(forms.ModelForm):
    class Meta:
        model = Group

    def __init__(self, *args, **kwargs):
        super(GroupAdminForm, self).__init__(*args, **kwargs)
        self.fields['header'].widget = TinyMCE(attrs={'cols':80, 'rows':20})
        self.fields['detail'].widget = TinyMCE(attrs={'cols':80, 'rows':20})
        self.fields['footer'].widget = TinyMCE(attrs={'cols':80, 'rows':20})
        self.fields['parent'].queryset = Group.objects.exclude(id=self.instance.id)
        
        
#		if self.instance.id:
#			try:
#				top_group = self.instance.report.group_set.get(top_group=True)
#				if self.instance != top_group:
#					self.fields['parent_group'].initial = top_group
#			except:
#				self.fields['top_group'].initial = True		
                #self.instance.group_set.g
                #if 
            #	pass
                #self.field['top_group
                #print "No top"
            #self.fields['parent_group'].value ='1'

    
class GroupInline(admin.StackedInline):
    model = Group
    extra = 1
    allow_add = True
    form = GroupAdminForm

    
#class ParameterInline(admin.StackedInline):
#    model = Parameter
#    extra = 1
#    allow_add = True


class ReportAdminForm(forms.ModelForm):
    class Meta:
        model = Report

    def __init__(self, *args, **kwargs):
        super(ReportAdminForm, self).__init__(*args, **kwargs)
        self.fields['page_header'].widget = TinyMCE(attrs={'cols':80, 'rows':20})
        self.fields['page_footer'].widget = TinyMCE(attrs={'cols':80, 'rows':20})

        
class ReportAdmin(admin.ModelAdmin):
    inlines = [GroupInline]#, ParameterInline]
    form = ReportAdminForm

    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'extra_tags', 'css_style', 'page_header', 'page_footer')
        }),
        (_(u'Data source'), {
            'fields': ('model', 'queryset')
        }),
    )    


admin.site.register(Report, ReportAdmin)
admin.site.register(ModelReportRelationship)
