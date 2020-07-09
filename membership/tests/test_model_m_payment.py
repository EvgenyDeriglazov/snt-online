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
from membership.models import *
from django.contrib.auth.models import User
from membership.validators import *
import datetime

class MPaymentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        ChairMan.objects.create(
            first_name="Сергей",
            middle_name="Сергеевич",
            last_name="Сергеев",
            join_date=datetime.date.today(),
            )
        Snt.objects.create(
            name='Бобровка',
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
            plot_area=600,
            snt=Snt.objects.get(id=1),
            owner=Owner.objects.get(id=1),
            )
        MRate.objects.create(
            date=datetime.date.today(),
            year_period='2020',
            rate=500,
            snt=Snt.objects.get(id=1),
            )
        MPayment.objects.create(
            year_period='2020',
            land_plot=LandPlot.objects.get(id=1),
            status='not_paid',
            )
        
    # Test functions
    def test_payment_date_field(self):
        obj = MPayment.objects.get(id=1)
        field = obj._meta.get_field('payment_date')
        self.assertEqual(field.verbose_name, "Дата оплаты")
        self.assertEqual(field.help_text, "Фактическая дата оплаты")
        self.assertEqual(field.blank, True)
        self.assertEqual(field.null, True)
        self.assertEqual(obj.payment_date, None)

    def test_year_period_field(self):
        obj = MPayment.objects.get(id=1)
        field = obj._meta.get_field('year_period')
        self.assertEqual(field.verbose_name, "Год")
        self.assertEqual(field.max_length, 4)
        self.assertEqual(field.help_text, "Укажите год в виде 4-х значного числа")
        self.assertEqual(
            field.validators[0:2],
            [validate_number, validate_year_period_min_length]
            )
        self.assertEqual(obj.year_period, '2020')

    def test_month_period_field(self):
        obj = MPayment.objects.get(id=1)
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
        #self.assertEqual(field.blank, True)
        self.assertEqual(field.choices, MONTH_PERIOD_CHOICES)
        self.assertEqual(field.default, '')
        self.assertEqual(obj.month_period, '')

    def test_rate_field(self):
        obj = MPayment.objects.get(id=1)
        field = obj._meta.get_field('rate')
        self.assertEqual(field.verbose_name, "Размер взноса")
        self.assertEqual(
            field.help_text,
            "Размер членского взноса за сотку (100 м.кв)/рублей"
            )
        self.assertEqual(obj.rate, 500)

    def test_plot_area_field(self):
        obj = MPayment.objects.get(id=1)
        field = obj._meta.get_field('plot_area')
        self.assertEqual(field.verbose_name, "Площадь участка")
        self.assertEqual(field.help_text, "Площадь участка в квадратных метрах")
        self.assertEqual(obj.plot_area, 600)

    def test_amount_field(self):
        obj = MPayment.objects.get(id=1)
        field = obj._meta.get_field('amount')
        self.assertEqual(field.verbose_name, "Сумма")
        self.assertEqual(field.help_text, "Сумма взноса к оплате")
        self.assertEqual(field.max_digits, 7)
        self.assertEqual(field.decimal_places, 2)
        self.assertEqual(obj.amount, Decimal(3000.00))

    def test_land_plot_field(self):
        obj = MPayment.objects.get(id=1)
        plot_obj = LandPlot.objects.get(id=1)
        field = obj._meta.get_field('land_plot')
        #on_delete = obj._meta.get_field('owner').on_delete
        self.assertEqual(field.verbose_name, "Участок")
        self.assertEqual(field.help_text, "Выберите участок")
        self.assertEqual(field.null, True)
        #self.assertEqual(on_delete, models.SET_NULL)
        self.assertEqual(obj.land_plot, plot_obj)

    def test_status_field(self):
        obj = MPayment.objects.get(id=1)
        field = obj._meta.get_field('status')
        STATUS_CHOICES = [
            ('not_paid', 'Неоплачено'),
            ('paid', 'Оплачено'),
            ('payment_confirmed', 'Оплата подтверждена'),
            ]
        #on_delete = obj._meta.get_field('owner').on_delete
        self.assertEqual(field.verbose_name, "Статус")
        self.assertEqual(field.max_length, 17)
        self.assertEqual(field.choices, STATUS_CHOICES)
        self.assertEqual(field.default, 'not_paid')
        self.assertEqual(field.help_text, "Статус оплаты")
        #self.assertEqual(on_delete, models.SET_NULL)
        self.assertEqual(obj.status, 'not_paid')

    def test_meta_options(self):
        self.assertEquals(MPayment._meta.verbose_name, "членский взнос")
        self.assertEquals(MPayment._meta.verbose_name_plural, "членские взносы")
        self.assertEquals(len(MPayment._meta.constraints), 1)
        self.assertEquals(
            MPayment._meta.constraints[0].fields,
            ('year_period','month_period', 'land_plot')
            )
        self.assertEquals(
            MPayment._meta.constraints[0].name,
            'membership_mpayment_year_month_period_land_plot_unique_constraint'
            )
   
    def test_str_method(self):
        obj = MPayment.objects.get(id=1)
        object_name = f"{obj.year_period} {obj.land_plot.plot_number}"
        self.assertEquals(object_name, obj.__str__())
        # or self.assertEquals(object_name, str(obj))
 
    def test_get_absolute_url(self):
        obj = MPayment.objects.get(id=1)
        self.assertEquals(obj.get_absolute_url(), "/data/land-plot-detail/1")
    
    def test_calculate_year_period(self):
        """Test for calculate() custom method with year period."""
        #Test rate change
        obj = MPayment.objects.get(id=1)
        MRate.objects.filter(id=1).update(rate=1000)
        self.assertEqual(obj.amount, Decimal(3000.00))
        obj.calculate()
        self.assertEqual(obj.amount, Decimal(6000.00))
        self.assertEqual(obj.rate, Decimal(1000.00))
        # Test plot area change
        LandPlot.objects.filter(id=1).update(plot_area=1200)
        obj = MPayment.objects.get(id=1)
        obj.calculate()
        self.assertEqual(obj.plot_area, 1200)
        self.assertEqual(obj.amount, Decimal(12000.00))
    
    def test_calculate_year_month_period(self):
        """Test for calculate() custom method with year-month period."""
        #Test rate and month period change
        MRate.objects.filter(id=1).update(rate=100, month_period='Jan')
        MPayment.objects.filter(id=1).update(month_period='Jan')
        obj = MPayment.objects.get(id=1)
        self.assertEqual(obj.amount, Decimal(3000.00))
        obj.calculate()
        self.assertEqual(obj.amount, Decimal(600.00))
        self.assertEqual(obj.rate, Decimal(100.00))
        # Test plot area change
        LandPlot.objects.filter(id=1).update(plot_area=1200)
        obj = MPayment.objects.get(id=1)
        obj.calculate()
        self.assertEqual(obj.plot_area, 1200)
        self.assertEqual(obj.amount, Decimal(1200.00))
    
    def test_save(self):
        """Test for save() custom methods."""
        # Check for status='not_paid'
        MRate.objects.create(
            date=datetime.date.today(),
            year_period='2020',
            month_period='Jan',
            rate=50,
            snt=Snt.objects.get(id=1),
            )
        MPayment.objects.create(
            year_period='2020',
            month_period='Jan',
            land_plot=LandPlot.objects.get(id=1),
            )
        obj = MPayment.objects.get(id=2)
        self.assertEqual(obj.plot_area, 600)
        self.assertEqual(obj.rate, Decimal(50.00))
        self.assertEqual(obj.amount, 300)
        # Check for status='paid'
        MRate.objects.filter(id=2).update(
            rate=100,
            )
        MPayment.objects.filter(id=2).update(
            status='paid',
            )
        self.assertEqual(obj.plot_area, 600)
        self.assertEqual(obj.rate, Decimal(50.00))
        self.assertEqual(obj.amount, 300)
        # Check for status='payment_confirmed'
        MRate.objects.filter(id=2).update(
            rate=150,
            )
        MPayment.objects.filter(id=2).update(
            status='payment_confirmed',
            )
        self.assertEqual(obj.plot_area, 600)
        self.assertEqual(obj.rate, Decimal(50.00))
        self.assertEqual(obj.amount, 300)
        

        
