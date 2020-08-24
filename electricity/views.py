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
        context['e_counter'] = e_counter(context['land_plot'])
        context['e_counter_record'] = latest_e_counter_record(
            context['e_counter'], context['land_plot']
            )
        context['e_payment'] = latest_e_payment(context['land_plot'])
        return context

# Helper functions
def latest_e_counter_record(e_counter, land_plot):
    """Returns latest e_counter_record."""
    try:
        return ECounterRecord.objects.filter(
            land_plot__exact=land_plot,
            e_counter__exact=e_counter,
            ).latest('rec_date')
    except ECounterRecord.DoesNotExist:
        return None

def latest_e_payment(land_plot):
    """Returns latest e_payment."""
    try:
        return EPayment.objects.filter(
            land_plot__exact=land_plot,
            ).latest('payment_date')
    except EPayment.DoesNotExist:
        return None

def e_counter(land_plot):
	"""Returns land_plot's e_counter."""
	try:
		return land_plot.ecounter
	except LandPlot.ecounter.RelatedObjectDoesNotExist:
		return None
