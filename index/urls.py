from django.urls import path
from index.views import *

urlpatterns = [
	path('', InfoPage.as_view(), name='info'),
	path('<int:pk>/', InfoDetailsPage.as_view(), name='info-details')

]
