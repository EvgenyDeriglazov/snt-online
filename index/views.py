from django.shortcuts import render
from index.models import *

# Create your views here.
def homepage(request):
    """View function for home page of site."""
    snt = Snt.objects.all()
    if len(snt) > 0:
        snt_name = snt[0].name 
    else:
        snt_name = "SNT Online"
    
    
    context = {
        'snt_name': snt_name,
    }

    return render(request, 'homepage.html', context=context)
