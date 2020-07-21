from django.shortcuts import render
from index.models import *

# Create your views here.
def homepage(request):
    """View function for home page of site."""
    context = {}
    snt = Snt.objects.all()
    info_list = Info.objects.filter(
        status__exact='published',
        ).order_by('-pub_date')
    #land_plot_list = snt[0].entry_set.all()
    if len(snt) > 0:
        context['snt_name'] = snt[0].name
        context['snt_address'] = snt[0].address
    else:
        context['snt_name'] = "СНТ Онлайн"
        context['snt_address'] = "Адрес СНТ Онлайн"
    
    #if len(info_list) > 0:
    #    context['info_list'] = info_list

    #context['land_plots_count'] = len(land_plot_list)

    return render(request, 'homepage.html', context=context)

def info(request):
    """View function for information page of site."""
    context = {}
    snt = Snt.objects.all()
    info_list = Info.objects.filter(
        status__exact='published',
        ).order_by('-pub_date')
    #land_plot_list = snt[0].entry_set.all()
    if len(snt) > 0:
        context['snt_name'] = snt[0].name
        context['snt_address'] = snt[0].address
    else:
        context['snt_name'] = "СНТ Онлайн"
        context['snt_address'] = "Адрес СНТ Онлайн"

    return render(request, 'info.html', context=context)
