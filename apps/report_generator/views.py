from django.shortcuts import get_object_or_404

from models import Report
from api import generate_report


def report_render(request, report_id):
    report = get_object_or_404(Report, pk=report_id)
    return generate_report(request, report)

def report_preview(request, report_id):
    report = get_object_or_404(Report, pk=report_id)
    return generate_report(request, report, mode='html')    
    
    
