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

class SntModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        ChairMan.objects.create(
            first_name='Иван',
            middle_name='Иванович',
            last_name='Иванов',
        )
        Snt.objects.create(
            name='СНТ Бобровка',
            personal_acc='01234567898765432101',
            bank_name='Банк',
            bic='123456789',
            corresp_acc='01234567898765432101',
            inn='0123456789',
            kpp='123456789',
            chair_man=ChairMan.objects.get(id=1),
        )
    # Test functions
    def test_name_field(self):
        snt = Snt.objects.get(id=1)
        field_label = snt._meta.get_field('name').verbose_name
        help_text = snt._meta.get_field('name').help_text
        max_length = snt._meta.get_field('name').max_length
        self.assertEquals(field_label, 'Наименование СНТ')   
        self.assertEqual(max_length, 200)
        self.assertEqual(help_text, 'Полное название СНТ')

    def test_personal_acc_field(self):
        snt = Snt.objects.get(id=1)
        field_label = snt._meta.get_field('personal_acc').verbose_name
        max_length = snt._meta.get_field('personal_acc').max_length
        help_text = snt._meta.get_field('personal_acc').help_text
        self.assertEqual(field_label, 'Номер расчетного счета')
        self.assertEqual(max_length, 20)
        self.assertEqual(help_text, 'Номер расчетного счета (20-и значное число)')

    def test_bank_name_field(self):
        snt = Snt.objects.get(id=1)
        field_label = snt._meta.get_field('bank_name').verbose_name
        max_length = snt._meta.get_field('bank_name').max_length
        help_text = snt._meta.get_field('bank_name').help_text
        self.assertEqual(field_label, 'Наименование банка получателя')
        self.assertEqual(max_length, 45)
        self.assertEqual(help_text, 'Наименование банка получателя')

    def test_bic_field(self):
        snt = Snt.objects.get(id=1)
        field_label = snt._meta.get_field('bic').verbose_name
        max_length = snt._meta.get_field('bic').max_length
        help_text = snt._meta.get_field('bic').help_text
        self.assertEqual(field_label, 'БИК')
        self.assertEqual(max_length, 9)
        self.assertEqual(help_text, 'БИК (9-и значное число)')

    def test_corresp_acc_field(self):
        snt = Snt.objects.get(id=1)
        field_label = snt._meta.get_field('corresp_acc').verbose_name
        max_length = snt._meta.get_field('corresp_acc').max_length
        help_text = snt._meta.get_field('corresp_acc').help_text
        self.assertEqual(field_label, 'Номер кор./счета')
        self.assertEqual(max_length, 20)
        self.assertEqual(help_text, 'Номер кор./счета (20-и значное число)')

    def test_inn_field(self):
        snt = Snt.objects.get(id=1)
        field_label = snt._meta.get_field('inn').verbose_name
        max_length = snt._meta.get_field('inn').max_length
        help_text = snt._meta.get_field('inn').help_text
        self.assertEqual(field_label, 'ИНН')
        self.assertEqual(max_length, 10)
        self.assertEqual(help_text, 'ИНН (10-и значное число)')

    def test_kpp_field(self):
        snt = Snt.objects.get(id=1)
        field_label = snt._meta.get_field('kpp').verbose_name
        max_length = snt._meta.get_field('kpp').max_length
        help_text = snt._meta.get_field('kpp').help_text
        self.assertEqual(field_label, 'КПП')
        self.assertEqual(max_length, 9)
        self.assertEqual(help_text, 'КПП (9-и значное число)')

    def test_chair_man_field(self):
        snt = Snt.objects.get(id=1)
        ch_m_obj = ChairMan.objects.get(id=1)
        field_label = snt._meta.get_field('chair_man').verbose_name
        help_text = snt._meta.get_field('chair_man').help_text
        self.assertEqual(snt.chair_man, ch_m_obj)
        self.assertEqual(field_label, 'председатель')
        self.assertEqual(help_text, 'Председатель садоводства')
    
    def test_object_name(self):
        snt = Snt.objects.get(id=1)
        object_name = f'{snt.name}'
        self.assertEquals(object_name, str(snt))

    def test_get_absolute_url(self):
        snt = Snt.objects.get(id=1)
        self.assertEquals(snt.get_absolute_url(), '/data/snt-detail/1')

    def test_verbose_names(self):
        self.assertEquals(Snt._meta.verbose_name, 'СНТ')
        self.assertEquals(Snt._meta.verbose_name_plural, 'СНТ')