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

