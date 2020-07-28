from django.shortcuts import render
from django.views.generic import ListView, DetailView
from index.models import *

# Create your views here.
class HomePage(ListView):
    """Class based view to display homepage."""
    model = Snt
    template_name = "home_page.html"
    context_object_name = "snt_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['land_plots_count'] = LandPlot.objects.count()
        return context

class InfoPage(ListView):
    """Class based view to display Info model page."""
    model = Snt
    template_name = "info_page.html"
    context_object_name = "snt_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['info_list'] = Info.objects.filter(
            status__exact='published',
            ).order_by('-pub_date')
        return context

class InfoDetailsPage(DetailView):
    """Class based view to display Info model details page."""
    model = Info
    template_name = "info_details_page.html"
    context_object_name = "info_details"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['snt_list'] = Snt.objects.all()
        return context


class SntBankDetailsPage(ListView):
    """Class based view to display Snt bank details page."""
    model = Snt
    template_name = "snt_bank_details_page.html"
    context_object_name = "snt_list"

class SntContactsPage(ListView):
    """Class based view to display Snt contacts."""
    model = Snt
    template_name = "snt_contacts_page.html"
    context_object_name = "snt_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if ChairMan.objects.filter(leave_date__isnull=True).exists():
            context['chair_man'] = ChairMan.objects.filter(
                leave_date__isnull=True).get()
        if Accountant.objects.filter(leave_date__isnull=True).exists():
            context['accountant'] = Accountant.objects.filter(
                leave_date__isnull=True).get()
        return context

class DocsPage(ListView):
    """Class based view to display Docs."""
    model = Snt
    template_name = "docs_page.html"
    context_object_name = "snt_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if Docs.objects.filter(status__exact='published').exists():
            context['docs_list'] = Docs.objects.filter(
                status__exact='published').order_by('-upload_date')
        return context

class DocsDetailsPage(DetailView):
    """Class based view to display Docs details page."""
    model = Docs
    template_name = "docs_details_page.html"
    context_object_name = "docs_details"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['snt_list'] = Snt.objects.all()
        return context
