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
    """Class based view to display homepage."""
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
        context['chair_man'] = ChairMan.objects.filter(
            leave_date__isnull=True)
        return context
