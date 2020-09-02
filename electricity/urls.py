from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from electricity.views import *

urlpatterns = [
	path('electricity/', ElectricityPage.as_view(), name='electricity'),
	path(
        'electricity/record-id-<int:record_id>/',
        ECounterRecordDetailsPage.as_view(),
        name='e-counter-record-details'
        ),
    path(
        'electricity/new-record/',
        CreateNewECounterRecordPage.as_view(),
        name='new-e-counter-record'
        ),
]

urlpatterns += static(
    settings.STATIC_URL,
    documents_root=settings.STATIC_ROOT,
)
