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
from index.models import *

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
        obj = ChairMan.objects.get(id=1)
        field_label = obj._meta.get_field('first_name').verbose_name
        max_length = obj._meta.get_field('first_name').max_length
        validators = obj._meta.get_field('first_name').validators
        help_text = obj._meta.get_field('first_name').help_text
        self.assertEquals(field_label, "Имя")
        self.assertEquals(max_length, 50)
        self.assertEquals(validators[0:1], [validate_human_names])
        self.assertEquals(help_text, "Введите имя")

    def test_middle_name_field(self):
        obj = ChairMan.objects.get(id=1)
        field_label = obj._meta.get_field('middle_name').verbose_name
        max_length = obj._meta.get_field('middle_name').max_length
        validators = obj._meta.get_field('middle_name').validators
        help_text = obj._meta.get_field('middle_name').help_text
        self.assertEquals(field_label, "Отчество")
        self.assertEquals(max_length, 50)
        self.assertEquals(validators[0:1], [validate_human_names])
        self.assertEquals(help_text, "Введите отчество")
    
    def test_last_name_field(self):
        obj = ChairMan.objects.get(id=1)
        field_label = obj._meta.get_field('last_name').verbose_name
        max_length = obj._meta.get_field('last_name').max_length
        validators = obj._meta.get_field('last_name').validators
        help_text = obj._meta.get_field('last_name').help_text
        self.assertEquals(field_label, "Фамилия")
        self.assertEquals(max_length, 50)
        self.assertEquals(validators[0:1], [validate_human_names])
        self.assertEquals(help_text, "Введите фамилию")

    def test_phone_field(self):
        pass

    def test_email_field(self):
        pass
        
    def test_object_name(self):
        obj = ChairMan.objects.get(id=1)
        object_name = f'{obj.last_name} {obj.first_name} {obj.middle_name}'
        self.assertEquals(object_name, str(obj))

    def test_get_absolute_url(self):
        obj = ChairMan.objects.get(id=1)
        self.assertEquals(obj.get_absolute_url(), '/data/chairman-detail/1')

    def test_verbose_names(self):
        self.assertEquals(ChairMan._meta.verbose_name, 'председатель')
        self.assertEquals(ChairMan._meta.verbose_name_plural, 'председатели')
