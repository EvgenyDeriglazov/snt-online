from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.forms import AuthenticationForm
#from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from index.models import *
from electricity.models import *
from electricity.forms import *
from index.views import get_model_by_user, LandPlotPage
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

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
            context['form'] = CreateEPaymentForm(instance=context['record'])
            if isinstance(user_model_instance, Owner):
                context['land_plots'] = user_model_instance.landplot_set.all()
            else:
                context['land_plots'] = None
            return context
        else:
            raise Http404("Такой страницы не существует")

    def post(self, request, *args, **kwargs):
        if 'record_id' in kwargs:
            e_record = ECounterRecord.objects.get(id=kwargs['pk'])
            #form = CreateEPaymentForm(request.POST)
            e_payment = e_record.create_e_payment()
            return HttpResponseRedirect(
                reverse(
                    'e-counter-record-details', kwargs={
                        'record_id': kwargs['record_id'],
                        'pk': kwargs['pk'],
                        }
                    )
                )
        else:
            raise Http404("Данные записи не найдены")

class CreateNewECounterRecordPage(LandPlotPage):
    """View to create new ECounterRecord by owner."""
    template_name = "create_new_e_counter_record_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['e_counter'] = e_counter(context['land_plot'])
        context['form'] = create_e_counter_record_form(
            context['e_counter'], context['land_plot']
            )           
        return context
    
    def post(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            land_plot = get_object_or_404(LandPlot, pk=kwargs['pk'])
            e_counter_obj = e_counter(land_plot)
            if e_counter_obj == None:
                raise Http404("Счетчик не найден")
            form = create_e_counter_record_form(
                e_counter_obj, land_plot, request.POST,
                )
        else:
            raise Http404("Данные участка не найдены")
        if form.is_valid():
            new_rec = form.save()
            return HttpResponseRedirect(
                reverse(
                    'e-counter-record-details', kwargs={
                        'record_id': new_rec.id, 'pk': new_rec.land_plot.id}
                    )
                )
        else:
            context = {}
            context['land_plot'] = form.instance.land_plot
            context['snt_list'] = Snt.objects.all()
            context['auth_form'] = AuthenticationForm 
            user_model_instance = get_model_by_user(self.request.user)
            context['user_name'] = str(user_model_instance)        
            context['e_counter'] = form.instance.e_counter
            context['form'] = form
            if isinstance(user_model_instance, Owner):
                context['land_plots'] = user_model_instance.landplot_set.all()
            else:
                context['land_plots'] = None

            return render(request, self.template_name, context)

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
        ).order_by('-rec_date')

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

def create_e_counter_record_form(e_counter, land_plot, request=None):
    """Returns single or double NewECounterRecordForm depending
    on electrical counter model type."""
    if e_counter and e_counter.model_type == "single":
        return CreateSingleECounterRecordForm(
            request,
            initial={'e_counter': e_counter, 'land_plot': land_plot}
            )
    elif e_counter and e_counter.model_type == "double":
        return CreateDoubleECounterRecordForm(
            request,
            initial={'e_counter': e_counter, 'land_plot': land_plot}
            ) 
