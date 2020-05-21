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
from membership.models import *
from index.models import *
from django.contrib.auth.models import User
from membership.validators import *
import datetime

class MRateModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        ChairMan.objects.create(
            first_name="Сергей",
            middle_name="Сергеевич",
            last_name="Сергеев",
            join_date=datetime.date.today(),
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
        Owner.objects.create(
            first_name="Сергей",
            middle_name="Сергеевич",
            last_name="Сергеев",
            join_date=datetime.date.today(),
            )
        LandPlot.objects.create(
            plot_number="10",
            plot_area=6000,
            snt=Snt.objects.get(id=1),
            owner=Owner.objects.get(id=1),
            )
        MRate.objects.create(
            date=datetime.date.today(),
            year_period="2020",
            month_period="",
            rate=1000,
            snt=Snt.objects.get(id=1),
            )
    # Test functions
    def test_date_field(self):
        obj = MRate.objects.get(id=1)
        field = obj._meta.get_field('date')
        self.assertEqual(field.verbose_name, "Дата")
        self.assertEqual(field.help_text, "Укажите дату ввода тарифа")
        self.assertEqual(obj.date, datetime.date.today())

    def test_year_period_field(self):
        obj = MRate.objects.get(id=1)
        field = obj._meta.get_field('year_period')
        self.assertEqual(field.verbose_name, "Год")
        self.assertEqual(field.max_length, 4)
        self.assertEqual(
            field.help_text,
            "Укажите год периода для произведения расчета"
            + " в виде 4-х значного числа"
            )
        self.assertEqual(
            field.validators[0:2],
            [validate_number, validate_year_period_min_length]
            )
        self.assertEqual(obj.year_period, '2020')

    def test_month_period_field(self):
        obj = MRate.objects.get(id=1)
        field = obj._meta.get_field('month_period')
        MONTH_PERIOD_CHOICES = [
        ('', ''),
        ('Jan', 'Январь'),
        ('Feb', 'Февраль'),
        ('Mar', 'Март'),
        ('Apr', 'Апрель'),
        ('May', 'Май'),
        ('Jun', 'Июнь'),
        ('Jul', 'Июль'),
        ('Aug', 'Август'),
        ('Sep', 'Сентябрь'),
        ('Oct', 'Октябрь'),
        ('Nov', 'Ноябрь'),
        ('Dec', 'Декабрь'),
        ]
        self.assertEqual(field.verbose_name, "Месяц")
        self.assertEqual(field.max_length, 3)
        self.assertEqual(
            field.help_text,
            "Выберите месяц, если начисления"
            + " членских взносов расчитываются помесячно"
            )
        self.assertEqual(field.blank, True)
        self.assertEqual(field.choices, MONTH_PERIOD_CHOICES)
        self.assertEqual(field.default, '')
        self.assertEqual(obj.month_period, '')

    def test_rate_field(self):
        obj = MRate.objects.get(id=1)
        field = obj._meta.get_field('rate')
        self.assertEqual(field.verbose_name, "Размер взноса")
        self.assertEqual(
            field.help_text,
            "Укажите размер членского взноса для" 
            + " выбранного периода в рублях за сотку (100 м.кв)"
            )
        self.assertEqual(obj.rate, 1000)

    def test_snt_field(self):
        obj = MRate.objects.get(id=1)
        snt_obj = Snt.objects.get(id=1)
        field = obj._meta.get_field('snt')
        self.assertEqual(field.null, True)
        self.assertEqual(field.verbose_name, "СНТ")
        self.assertEqual(
            field.help_text,
            "Укажите СНТ для которого будет применен тариф"
            )
        self.assertEqual(obj.snt, snt_obj)


    def test_meta_options(self):
        self.assertEquals(MRate._meta.verbose_name, "Тариф (членский взнос)")
        self.assertEquals(
            MRate._meta.verbose_name_plural,
            "Тарифы (членский взнос)"
            )
        self.assertEquals(
            MRate._meta.constraints[0].fields,
            ('year_period','month_period')
            )
   
    def test_str_method(self):
        obj = MRate.objects.get(id=1)
        object_name = f"{obj.year_period} {obj.month_period}"
        self.assertEquals(object_name, obj.__str__())
        # or self.assertEquals(object_name, str(obj))
 
    def test_get_absolute_url(self):
        obj = MRate.objects.get(id=1)
        self.assertEquals(obj.get_absolute_url(), "/data/land-plot-detail/1")
