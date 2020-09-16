from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from membership.views import *

urlpatterns = [
	path('membership/', MembershipPage.as_view(), name='membership')

]

urlpatterns += static(
    settings.STATIC_URL,
    documents_root=settings.STATIC_ROOT,
)