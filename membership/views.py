from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.forms import AuthenticationForm
#from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from index.models import *
from membership.models import *
from membership.forms import *
from index.views import get_model_by_user, LandPlotPage
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.db import IntegrityError

# Create your views here.

class MembershipPaymentsPage(LandPlotPage):
    """View to display membership payments page as list of items."""
    template_name = "membership_payments_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['payment_data_list'] = MPayment.objects.filter(
        	land_plot__exact=context['land_plot']
        	).order_by('-year_period')

        return context

class TargetPaymentsPage(LandPlotPage):
    """View to display membership payments page as list of items."""
    template_name = "target_payments_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['payment_data_list'] = TPayment.objects.filter(
        	land_plot__exact=context['land_plot']
        	).order_by('-payment_date')

        return context

class MembershipPaymentDetailsPage(LoginRequiredMixin, DetailView):
    """View to display electrical counter records detail page."""
    model = MPayment
    template_name = "membership_payment_details_page.html"
    context_object_name = "m_payment"
    pk_url_kwarg = "m_payment_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if context['m_payment'].land_plot.owner.user == self.request.user:
            context['snt_list'] = Snt.objects.all()
            context['land_plot'] = context['m_payment'].land_plot
            context['auth_form'] = AuthenticationForm
            user_model_instance = get_model_by_user(self.request.user)
            context['user_name'] = str(user_model_instance)
            context['qr_pay_data'] = context['m_payment'].create_qr_text()
            context['form'] = NoFieldsMPaymentForm()
            if isinstance(user_model_instance, Owner):
                context['land_plots'] = user_model_instance.landplot_set.all()
            else:
                context['land_plots'] = None
            return context
        else:
            raise Http404("Такой страницы не существует")

    def post(self, request, *args, **kwargs):
        if 'm_payment_id' in kwargs:
            m_payment = MPayment.objects.get(id=kwargs['m_payment_id'])
            if m_payment.status == "not_paid":
                plot_id = m_payment.land_plot.id
                m_payment.paid()
                return HttpResponseRedirect(
                    reverse(
                        'membership-payment-details',
                        kwargs={
                        	'plot_id': plot_id, 'm_payment_id': m_payment.id
                        	}
                        )
                    )
            else:
                raise Http404("Статус записи изменился")
        else:
            raise Http404("Данные записи не найдены")