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
    path(
        'electricity/record-id-<int:record_id>/delete/',
        DeleteECounterRecordPage.as_view(),
        name='delete-e-counter-record'
        ),
    path(
    	'electricity/e-payment-id-<int:e_payment_id>/',
    	EPaymentDetailsPage.as_view(),
    	name='e-payment-details',
    	),
]

urlpatterns += static(
    settings.STATIC_URL,
    documents_root=settings.STATIC_ROOT,
)
