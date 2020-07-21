from django.shortcuts import render
from index.models import *

# Create your views here.
def homepage(request):
    """View function for home page of site."""
    snt = Snt.objects.all()
    if len(snt) > 0:
        snt_name = snt[0].name
        snt_address = snt[0].address
    else:
        snt_name = "СНТ Онлайн"
        snt_address = "Адрес СНТ Онлайн"
    
    
    context = {
        'snt_name': snt_name,
        'snt_address': snt_address,
    }

    return render(request, 'homepage.html', context=context)
