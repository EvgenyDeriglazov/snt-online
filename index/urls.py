from django.urls import path
from index.views import InfoPage

urlpatterns = [
	path('', InfoPage.as_view(), name='info'),

]
