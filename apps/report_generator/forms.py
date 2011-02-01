from django import forms 
from django.utils.translation import ugettext_lazy as _

from generic_views.forms import DetailForm

from models import Report
                  
class ReportForm_view(DetailForm):
    class Meta:
        model = Report
