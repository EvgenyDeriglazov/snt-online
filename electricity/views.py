from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.forms import AuthenticationForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from index.models import *
from electricity.models import *
from index.views import get_model_by_user, LandPlotPage
# Create your views here.

class ElectricityPage(LandPlotPage):
    """View to display electricity page."""
    template_name = "electricity_page.html"
#    context_object_name = "snt_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['e_counter'] = context['land_plot'].ecounter
        return context
