# --- Collectstatic (ValueError: Missing staticfiles manifest entry...) ---
#  $python3 manage.py collectstatic
# --- Verbosity ---
#  $python3 manage.py test --verbosity (1-default, 0, 1, 2, 3)
# --- Run specific test modules ---
#  $python3 manage.py test data.tests
#  $python3 manage.py test data.tests.test_models
#  $python3 manage.py test data.tests.test_models.TestClass
# --- Coverage.py --- 
#  $coverage run --source='.' manage.py test <appname>
#  $coverage report

from django.test import TestCase
from index.models import *
import datetime

class SntModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        ChairMan.objects.create(
            first_name='Иван',
            middle_name='Иванович',
            last_name='Иванов',
            join_date=datetime.date.today()
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
            address="123СТАР",
            )
    # Test functions
    def test_name_field(self):
        obj = Snt.objects.get(id=1)
        field = obj._meta.get_field('name')
        self.assertEquals(field.verbose_name, "Название СНТ")   
        self.assertEqual(field.max_length, 200)
        self.assertEqual(field.help_text, "Полное название СНТ")
        self.assertEqual(obj.name, "СНТ Бобровка")

    def test_personal_acc_field(self):
        obj = Snt.objects.get(id=1)
        field = obj._meta.get_field('personal_acc')
        self.assertEqual(field.verbose_name, "Номер расчетного счета")
        self.assertEqual(field.max_length, 20)
        self.assertEqual(
            field.help_text,
            "Номер расчетного счета (20-и значное число)"
            )
        self.assertEqual(
            field.validators[0:2],
            [validate_number, validate_20_length]
            )
        self.assertEqual(obj.personal_acc, "01234567898765432101")

    def test_bank_name_field(self):
        obj = Snt.objects.get(id=1)
        field = obj._meta.get_field('bank_name')
        self.assertEqual(field.verbose_name, "Наименование банка получателя")
        self.assertEqual(field.max_length, 45)
        self.assertEqual(field.help_text, "Наименование банка получателя")
        self.assertEqual(obj.bank_name, "Банк")

    def test_bic_field(self):
        obj = Snt.objects.get(id=1)
        field = obj._meta.get_field('bic')
        self.assertEqual(field.verbose_name, "БИК")
        self.assertEqual(field.max_length, 9)
        self.assertEqual(field.help_text, "БИК (9-и значное число)")
        self.assertEqual(
            field.validators[0:2],
            [validate_number, validate_9_length],
            )
        self.assertEqual(obj.bic, "123456789")

    def test_corresp_acc_field(self):
        obj = Snt.objects.get(id=1)
        field = obj._meta.get_field('corresp_acc')
        self.assertEqual(field.verbose_name, "Номер кор./счета")
        self.assertEqual(field.max_length, 20)
        self.assertEqual(field.help_text, "Номер кор./счета (20-и значное число)")
        self.assertEqual(
            field.validators[0:2],
            [validate_number, validate_20_length],
            )
        self.assertEqual(obj.corresp_acc, "01234567898765432101")

    def test_inn_field(self):
        obj = Snt.objects.get(id=1)
        field = obj._meta.get_field('inn')
        self.assertEqual(field.verbose_name, "ИНН")
        self.assertEqual(field.max_length, 10)
        self.assertEqual(field.help_text, "ИНН (10-и значное число)")
        self.assertEqual(
            field.validators[0:2],
            [validate_number, validate_10_length],
            )
        self.assertEqual(obj.inn, "0123456789")

    def test_kpp_field(self):
        obj = Snt.objects.get(id=1)
        field = obj._meta.get_field('kpp')
        self.assertEqual(field.verbose_name, "КПП")
        self.assertEqual(field.max_length, 9)
        self.assertEqual(field.help_text, "КПП (9-и значное число)")
        self.assertEqual(
            field.validators[0:2],
            [validate_number, validate_9_length],
            )
        self.assertEqual(obj.kpp, "123456789")

    def test_address_field(self):
        obj = Snt.objects.get(id=1)
        field = obj._meta.get_field('address')
        self.assertEqual(field.verbose_name, "Адрес")
        self.assertEqual(field.max_length, 200)
        self.assertEqual(
            field.help_text, 
            "Полный адрес садоводства включая область и р-он",
            )
        self.assertEqual(obj.address, "123СТАР")
 
    def test_chair_man_field(self):
        obj = Snt.objects.get(id=1)
        ch_m_obj = ChairMan.objects.get(id=1)
        field = obj._meta.get_field('chair_man')
        self.assertEqual(field.verbose_name, "председатель")
        self.assertEqual(field.help_text, "председатель садоводства")
        self.assertEqual(obj.chair_man, ch_m_obj)

    def test_meta_options(self):
        self.assertEquals(Snt._meta.verbose_name, "СНТ")
        self.assertEquals(Snt._meta.verbose_name_plural, "СНТ")   

    def test_str_method(self):
        obj = Snt.objects.get(id=1)
        object_name = f"{obj.name}"
        self.assertEquals(object_name, obj.__str__())

    def test_get_absolute_url(self):
        obj = Snt.objects.get(id=1)
        self.assertEquals(obj.get_absolute_url(), "/data/obj-detail/1")

    # Custom functions tests
    def test_save_function(self):
        obj = Snt.objects.get(id=1)
        self.assertEquals(obj.save(), None)
        # Try to create new object and check
        obj2 = Snt.objects.create(
            name='тест',
            personal_acc='01234567898765432100',
            bank_name='Банк',
            bic='123456780',
            corresp_acc='01234567898765432100',
            inn='0123456780',
            kpp='123456780',
            chair_man=ChairMan.objects.get(id=1),
            address="123СТА0",
                )
        obj2.save()
        self.assertEquals(Snt.objects.count(), 1)
        # Try to update and check
        Snt.objects.filter(id=1).update(name='New name')
        self.assertEquals(Snt.objects.get(id=1).name, 'New name')
        # Try to update via object instance
        obj.name = 'xnew'
        obj.save()
        self.assertEquals(Snt.objects.get(id=1).name, 'xnew')



