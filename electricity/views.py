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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['e_counter'] = e_counter(context['land_plot'])
        context['payment_data_list'] = e_counter_records_with_e_payments_list(
        	context['e_counter'], context['land_plot']
        	)
        return context

class ECounterRecordsPage(LandPlotPage):
    """View to display electrical counter records page."""
    template_name = "e_counter_records_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['e_counter'] = e_counter(context['land_plot'])
        context['e_counter_records_list'] = ECounterRecord.objects.filter(
            e_counter__exact=context['e_counter'],
            land_plot__exact=context['land_plot'],
            )
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

def all_e_counter_records(e_counter, land_plot):
	"""Returns queryset of all ECounterRecords for land_plot and
	e_counter args."""
	return ECounterRecord.objects.filter(
		e_counter__exact=e_counter,
		land_plot__exact=land_plot,
		).order_by('rec_date')

def e_counter_records_with_e_payments_list(e_counter, land_plot):
	"""Returns list of lists with 2 items, e_counter_record
	and associated with it e_payment via one-to-one field.
	If e_payment DoesNotExist adds None value to list."""
	e_counter_records_list = all_e_counter_records(e_counter, land_plot)
	if len(e_counter_records_list) > 0:
		list_of_lists = []
		for i in e_counter_records_list:
			list_item = [i]
			try:
				list_item.append(i.epayment)
			except ECounterRecord.epayment.RelatedObjectDoesNotExist:
				list_item.append(None)
			list_of_lists.append(list_item)
		return list_of_lists
	else:
		return [[None, None]]

