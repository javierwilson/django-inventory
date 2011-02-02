from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType

from models import Report
from api import generate_report


def report_render(request, report_id, mode='pdf', app_label=None, model=None, pk=None):
    report = get_object_or_404(Report, pk=report_id)
    if app_label and model and pk:
        model_class = ContentType.objects.get(app_label=app_label, model=model).model_class()
        queryset = model_class.objects.filter(pk=pk)
    else:
        queryset=None

    return generate_report(request, report, mode=mode, queryset=queryset)
