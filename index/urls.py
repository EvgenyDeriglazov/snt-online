from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from index.views import *

urlpatterns = [
	path('', HomePage.as_view(), name='home'),
	#path('info/', InfoPage.as_view(), name='info'),
	#path('info/<int:pk>/', InfoDetailsPage.as_view(), name='info-details'),
	#path('docs/', DocsPage.as_view(), name='docs'),
    #path('docs/<int:pk>/', DocsDetailsPage.as_view(), name='docs-details'),
    path(
        'snt-bank-details/',
        SntBankDetailsPage.as_view(),
        name='snt-bank-details'
        ),
    path('contacts/', SntContactsPage.as_view(), name='snt-contacts'),
    path('plot-id-<int:plot_id>/', LandPlotPage.as_view(), name='land-plot'),
    path('plot-id-<int:plot_id>/', include('electricity.urls')),
    path('plot-id-<int:plot_id>/', include('membership.urls')),
]

urlpatterns += static(
    settings.STATIC_URL,
    documents_root=settings.STATIC_ROOT,
)
