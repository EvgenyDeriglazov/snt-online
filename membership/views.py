from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.forms import AuthenticationForm
#from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from index.models import *
from membership.models import *
#from membership.forms import *
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