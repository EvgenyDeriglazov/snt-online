# --- Collectstatic (ValueError: Missing staticfiles manifest entry...) ---
# python3 manage.py collectstatic
# --- Verbosity ---
# python3 manage.py test --verbosity (1-default, 0, 1, 2, 3)
# --- Run specific test modules ---
# python3 manage.py test data.tests
# python3 manage.py test data.tests.test_models
# python3 manage.py test data.tests.test_models.TestClass
# --- Coverage.py --- 
# coverage run --source='.' manage.py test <appname>
# coverage report

from django.test import TestCase
from data.models import *
from datetime import date
from decimal import *

class ChairManModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        ChairMan.objects.create(
            first_name='Иван',
            middle_name='Иванович',
            last_name='Иванов',
        )
    # Test functions
    def test_first_name_field(self):
        ch_m = ChairMan.objects.get(id=1)
        field_label = ch_m._meta.get_field('first_name').verbose_name
        max_length = ch_m._meta.get_field('first_name').max_length
        help_text = ch_m._meta.get_field('first_name').help_text
        self.assertEquals(field_label, "Имя")
        self.assertEquals(max_length, 50)
        self.assertEquals(help_text, "Введите имя")

    def test_middle_name_field(self):
        ch_m = ChairMan.objects.get(id=1)
        field_label = ch_m._meta.get_field('middle_name').verbose_name
        max_length = ch_m._meta.get_field('middle_name').max_length
        help_text = ch_m._meta.get_field('middle_name').help_text
        self.assertEquals(field_label, "Отчество")
        self.assertEquals(max_length, 50)
        self.assertEquals(help_text, "Введите отчество")
    
    def test_last_name_field(self):
        ch_m = ChairMan.objects.get(id=1)
        field_label = ch_m._meta.get_field('last_name').verbose_name
        max_length = ch_m._meta.get_field('last_name').max_length
        help_text = ch_m._meta.get_field('last_name').help_text
        self.assertEquals(field_label, "Фамилия")
        self.assertEquals(max_length, 50)
        self.assertEquals(help_text, "Введите фамилию")
        
    def test_object_name(self):
        ch_m = ChairMan.objects.get(id=1)
        object_name = f'{ch_m.last_name} {ch_m.first_name} {ch_m.middle_name}'
        self.assertEquals(object_name, str(ch_m))

    def test_get_absolute_url(self):
        ch_m = ChairMan.objects.get(id=1)
        self.assertEquals(ch_m.get_absolute_url(), '/data/chairman-detail/1')

    def test_verbose_names(self):
        self.assertEquals(ChairMan._meta.verbose_name, 'председатель')
        self.assertEquals(ChairMan._meta.verbose_name_plural, 'председатели')
