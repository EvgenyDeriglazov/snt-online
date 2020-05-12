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

class OwnerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Owner.objects.create(
            first_name="Сергей",
            middle_name="Сергеевич",
            last_name="Сергеев",
            status='p',
            start_owner_date=date(2020, 1, 1),
            end_owner_date=None,
        )
    # Test functions
    def test_first_name_field(self):
        owner_obj = Owner.objects.get(id=1)
        field_label = owner_obj._meta.get_field('first_name').verbose_name
        max_length = owner_obj._meta.get_field('first_name').max_length
        help_text = owner_obj._meta.get_field('first_name').help_text
        validators = owner_obj._meta.get_field('first_name').validators
        self.assertEquals(field_label, 'Имя')
        self.assertEquals(max_length, 50)
        self.assertEquals(help_text, 'Введите имя')
        self.assertEquals(validators[0:1], [validate_human_names])
        self.assertEquals(owner_obj.first_name, "Сергей")
       
    def test_middle_name_field(self):
        owner_obj = Owner.objects.get(id=1)
        field_label = owner_obj._meta.get_field('middle_name').verbose_name
        max_length = owner_obj._meta.get_field('middle_name').max_length
        help_text = owner_obj._meta.get_field('middle_name').help_text
        validators = owner_obj._meta.get_field('middle_name').validators
        self.assertEquals(field_label, 'Отчество')
        self.assertEquals(max_length, 50)
        self.assertEquals(help_text, 'Введите отчество')
        self.assertEquals(validators[0:1], [validate_human_names])
        self.assertEquals(owner_obj.middle_name, "Сергеевич")
    
    def test_last_name_field(self):
        owner_obj = Owner.objects.get(id=1)
        field_label = owner_obj._meta.get_field('last_name').verbose_name
        max_length = owner_obj._meta.get_field('last_name').max_length
        help_text = owner_obj._meta.get_field('last_name').help_text
        validators = owner_obj._meta.get_field('last_name').validators
        self.assertEquals(field_label, 'Фамилия')
        self.assertEquals(max_length, 50)
        self.assertEquals(help_text, 'Введите фамилию')
        self.assertEquals(validators[0:1], [validate_human_names])
        self.assertEquals(owner_obj.last_name, "Сергеев")
    
    def test_status_field(self):
        owner_obj = Owner.objects.get(id=1)
        OWNER_STATUS = [
            ('c', 'Настоящий'),
            ('p', 'Прежний'),
        ]
        field_label = owner_obj._meta.get_field('status').verbose_name
        max_length = owner_obj._meta.get_field('status').max_length
        owner_status = owner_obj._meta.get_field('status').choices
        defaults = owner_obj._meta.get_field('status').default
        help_text = owner_obj._meta.get_field('status').help_text
        self.assertEquals(field_label, 'Статус владельца')
        self.assertEquals(max_length, 1)
        self.assertEquals(owner_status, OWNER_STATUS)
        self.assertEquals(defaults, 'c')
        self.assertEquals(help_text, 'Статус владельца')
        self.assertEquals(owner_obj.status, 'p')
    
    def test_start_owner_date_field(self):
        owner_obj = Owner.objects.get(id=1)
        field_label = owner_obj._meta.get_field('start_owner_date').verbose_name
        self.assertEquals(field_label, 'дата начала владения')
        self.assertEquals(owner_obj.start_owner_date, date(2020, 1, 1))
    
    def test_end_owner_date_field(self):
        owner_obj = Owner.objects.get(id=1)
        field_label = owner_obj._meta.get_field('end_owner_date').verbose_name
        blank = owner_obj._meta.get_field('end_owner_date').blank
        null = owner_obj._meta.get_field('end_owner_date').null
        self.assertEquals(field_label, 'дата окончания владения')
        self.assertEquals(blank, True)
        self.assertEquals(null, True)
        self.assertEquals(owner_obj.end_owner_date, None)
    
    def test_object_name(self):
        obj = Owner.objects.get(id=1)
        obj_name = f'{obj.last_name} {obj.first_name} {obj.middle_name}'
        self.assertEquals(obj_name, obj.__str__())
        # or self.assertEquals(object_name, str(lp_obj))
    
    def test_get_absolute_url(self):
        obj = Owner.objects.get(id=1)
        self.assertEquals(obj.get_absolute_url(), '/data/owner-detail/1')

    def test_verbose_names(self):
        self.assertEquals(Owner._meta.verbose_name, 'владелец')
        self.assertEquals(Owner._meta.verbose_name_plural, 'владельцы')
 