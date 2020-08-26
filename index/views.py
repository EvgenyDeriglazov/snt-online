from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from django.http import Http404
from index.models import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

# Create your views here.
class HomePage(TemplateView):
    """Class based view to display homepage."""
    template_name = "home_page.html"
#    context_object_name = "snt_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['snt_list'] = Snt.objects.all()
        context['land_plots_count'] = LandPlot.objects.count()
        context['auth_form'] = AuthenticationForm
        user_model_instance = get_model_by_user(self.request.user)
        context['user_name'] = str(user_model_instance)
        if isinstance(user_model_instance, Owner):
            context['land_plots'] = user_model_instance.landplot_set.all()
        else:
            context['land_plots'] = None
        return context

class InfoPage(TemplateView):
    """Class based view to display Info model page."""
    template_name = "info_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['snt_list'] = Snt.objects.all()
        context['info_list'] = Info.objects.filter(
            status__exact='published',
            ).order_by('-pub_date')
        context['auth_form'] = AuthenticationForm
        user_model_instance = get_model_by_user(self.request.user)
        context['user_name'] = str(user_model_instance)
        if isinstance(user_model_instance, Owner):
            context['land_plots'] = user_model_instance.landplot_set.all()
        else:
            context['land_plots'] = None
        return context

class InfoDetailsPage(DetailView):
    """Class based view to display Info model details page."""
    model = Info
    template_name = "info_details_page.html"
    context_object_name = "info_details"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['snt_list'] = Snt.objects.all()
        context['auth_form'] = AuthenticationForm
        user_model_instance = get_model_by_user(self.request.user)
        context['user_name'] = str(user_model_instance)
        if isinstance(user_model_instance, Owner):
            context['land_plots'] = user_model_instance.landplot_set.all()
        else:
            context['land_plots'] = None
        return context


class SntBankDetailsPage(TemplateView):
    """Class based view to display Snt bank details page."""
    template_name = "snt_bank_details_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['snt_list'] = Snt.objects.all()
        context['auth_form'] = AuthenticationForm
        user_model_instance = get_model_by_user(self.request.user)
        context['user_name'] = str(user_model_instance)
        if isinstance(user_model_instance, Owner):
            context['land_plots'] = user_model_instance.landplot_set.all()
        else:
            context['land_plots'] = None
        return context

class SntContactsPage(TemplateView):
    """Class based view to display Snt contacts."""
    template_name = "snt_contacts_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['snt_list'] = Snt.objects.all()
        context['auth_form'] = AuthenticationForm
        user_model_instance = get_model_by_user(self.request.user)
        context['user_name'] = str(user_model_instance)
        if isinstance(user_model_instance, Owner):
            context['land_plots'] = user_model_instance.landplot_set.all()
        else:
            context['land_plots'] = None
        context['chair_man'] = context['snt_list'][0].chair_man
        context['accountant'] = context['snt_list'][0].accountant
        return context

class DocsPage(TemplateView):
    """Class based view to display Docs."""
    template_name = "docs_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['snt_list'] = Snt.objects.all()
        if Docs.objects.filter(status__exact='published').exists():
            context['docs_list'] = Docs.objects.filter(
                status__exact='published').order_by('-upload_date')
        context['auth_form'] = AuthenticationForm
        user_model_instance = get_model_by_user(self.request.user)
        context['user_name'] = str(user_model_instance)
        if isinstance(user_model_instance, Owner):
            context['land_plots'] = user_model_instance.landplot_set.all()
        else:
            context['land_plots'] = None
        context['chair_man'] = context['snt_list'][0].chair_man
        context['accountant'] = context['snt_list'][0].accountant
        return context

class DocsDetailsPage(DetailView):
    """Class based view to display Docs details page."""
    model = Docs
    template_name = "docs_details_page.html"
    context_object_name = "docs_details"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['snt_list'] = Snt.objects.all()
        context['auth_form'] = AuthenticationForm
        user_model_instance = get_model_by_user(self.request.user)
        context['user_name'] = str(user_model_instance)
        if isinstance(user_model_instance, Owner):
            context['land_plots'] = user_model_instance.landplot_set.all()
        else:
            context['land_plots'] = None
        context['chair_man'] = context['snt_list'][0].chair_man
        context['accountant'] = context['snt_list'][0].accountant
        return context

#@method_decorator(login_required, name='dispatch')
class LandPlotPage(LoginRequiredMixin, DetailView):
    """View to display Land Plot details page."""
    model = LandPlot
    template_name = "land_plot_page.html"
    context_object_name = "land_plot"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if context['land_plot'].owner.user == self.request.user: 
            context['snt_list'] = Snt.objects.all()
            context['auth_form'] = AuthenticationForm
            user_model_instance = get_model_by_user(self.request.user)
            context['user_name'] = str(user_model_instance)
            if isinstance(user_model_instance, Owner):
                context['land_plots'] = user_model_instance.landplot_set.all()
            else:
                context['land_plots'] = None
            return context
        else:
            raise Http404

# Re-use helper functions
def get_model_by_user(user):
    """Returns related model instance via one-to-one relationship
    to user. If model does not exist returns user.username.
    If user is not authenticated returns None."""
    if user.is_authenticated:
        try:
            return user.owner
        except Owner.DoesNotExist:
            pass
        try:
            return user.accountant
        except Accountant.DoesNotExist:
            pass
        try:
            return user.chairman
        except ChairMan.DoesNotExist:
            pass
        return user.username

def get_land_plots(user_model_instance):
    """Returns query set of land plots which belongs
    to model_instance."""
    if isinstance(user_model_instance, Owner):
        return user_model_instance.landplot_set.all()
