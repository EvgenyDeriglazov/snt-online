from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.forms import AuthenticationForm
from django.utils.decorators import method_decorator
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from index.models import *
from electricity.models import *
from electricity.forms import *
from index.views import get_model_by_user, LandPlotPage

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

class ECounterRecordDetailsPage(LoginRequiredMixin, DetailView):
    """View to display electrical counter records detail page."""
    model = ECounterRecord
    template_name = "e_counter_record_details_page.html"
    context_object_name = "record"
    pk_url_kwarg = "record_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if context['record'].land_plot.owner.user == self.request.user:
            context['snt_list'] = Snt.objects.all()
            context['land_plot'] = context['record'].land_plot
            context['auth_form'] = AuthenticationForm
            context['counter_type'] = context['record'].e_counter.model_type
            user_model_instance = get_model_by_user(self.request.user)
            context['user_name'] = str(user_model_instance)
            if isinstance(user_model_instance, Owner):
                context['land_plots'] = user_model_instance.landplot_set.all()
            else:
                context['land_plots'] = None
            return context
        else:
            raise Http404("Такой страницы не существует")

class CreateNewECounterRecordPage(LandPlotPage):
    """View to create new ECounterRecord by owner."""
    template_name = "create_new_e_counter_record.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['e_counter'] = e_counter(context['land_plot'])
        if self.request.method == 'POST':
            raise Http404("Ошибка")
            form = NewSingleECounterRecordForm(self.request.POST)#new_e_counter_record_form(context['e_counter'])(self.request.POST)
            if form.is_valid():
                raise Http404("Ошибка")
                if isinstance(form, NewSingleECounterRecordForm):
                    s_clean = form.cleaned_data['s']
                    ECounterRecord.objects.create(
                        t1=None,
                        t2=None,
                        s=s_clean,
                        e_counter=context['e_counter'],
                        land_plot=context['land_plot'],
                        )
                elif isinstance(form, NewDoubleECounterRecordForm):
                    pass
            else:
                raise Http404("Ошибка")
        else:
            context['form'] = new_e_counter_record_form(context['e_counter']) 

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

def new_e_counter_record_form(e_counter):
    """Returns single or double NewECounterRecordForm depending
    on electrical counter model type."""
    if e_counter and e_counter.model_type == "single":
        return NewSingleECounterRecordForm()
    elif e_counter and e_counter.model_type == "double":
        return NewDoubleECounterRecordForm()