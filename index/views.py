from django.shortcuts import render

# Create your views here.
def homepage(request):
    """View function for home page of site."""
    context = {
        'x': 5,
    }

    return render(request, 'homepage.html', context=context)
