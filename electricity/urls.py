from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from electricity.views import *

urlpatterns = [
	path('electricity/', ElectricityPage.as_view(), name='electricity'),
	path(
        'electricity/record-<int:id>',
        ECounterRecordDetailsPage.as_view(),
        name='e-counter-record-details'
        ),
]

urlpatterns += static(
    settings.STATIC_URL,
    documents_root=settings.STATIC_ROOT,
)
