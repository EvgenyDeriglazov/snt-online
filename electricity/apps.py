from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ElectricityConfig(AppConfig):
    name = 'electricity'
    verbose_name = _('э/энергия')
