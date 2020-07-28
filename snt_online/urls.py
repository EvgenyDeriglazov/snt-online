"""snt_online URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from index.views import *

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('info/', InfoPage.as_view(), name='info'),
    path('info/<int:pk>', InfoDetailsPage.as_view(), name='info-details'),
    path(
        'snt-bank-details/',
        SntBankDetailsPage.as_view(),
        name='snt-bank-details'
        ),
    path('docs/', DocsPage.as_view(), name='docs'),
    path('docs/<int:pk>', DocsDetailsPage.as_view(), name='docs-details'),
    path('contacts/', SntContactsPage.as_view(), name='snt-contacts'),
    path('accounts/', include('django.contrib.auth.urls')),
]

urlpatterns += static(
    settings.STATIC_URL,
    documents_root=settings.STATIC_ROOT,
)

