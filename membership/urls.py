from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from membership.views import *

urlpatterns = [
	path(
		'membership/',
		MembershipPaymentsPage.as_view(),
		name='membership'
		),
	path(
		'target/',
		TargetPaymentsPage.as_view(),
		name='target'
		),
]

urlpatterns += static(
    settings.STATIC_URL,
    documents_root=settings.STATIC_ROOT,
)