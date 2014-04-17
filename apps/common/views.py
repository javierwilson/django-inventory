from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView

def password_change_done(request):
    messages.success(request, _(u'Your password has been successfully changed.'))
    return redirect('home')

class ExtraContext(object):
    extra_context = {}
    extra_fields = {}
    list_filters = {}
    form_class = {}
    def get_context_data(self, **kwargs):
        context = super(ExtraContext, self).get_context_data(**kwargs)
        context.update(self.extra_context)
        if 'object' in context:
            if hasattr(self.queryset, 'get'):
                aform = self.form_class(instance=self.queryset.get(id=context['object'].pk))
                context['form'] = aform
        return context

class ExtraListView(ExtraContext, ListView):
    template_name="generic_list.html"
    pass

class ExtraDetailView(ExtraContext, DetailView):
    template_name="generic_detail.html"
    pass

class ExtraUpdateView(ExtraContext, UpdateView):
    pass

class ExtraCreateView(ExtraContext, CreateView):
    pass 

class ExtraDeleteView(ExtraContext, DeleteView):
    post_delete_redirect = ""
    template_name = "generic_confirm.html"
    pass
