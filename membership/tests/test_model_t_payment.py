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

class TPaymentModelTest(TestCase):
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
        TPayment.objects.create(
            target="Test target",
            amount=6000,
            land_plot=LandPlot.objects.get(id=1),
            status='not_paid',
            )
    # Test functions
    def test_payment_date_field(self):
        obj = TPayment.objects.get(id=1)
        field = obj._meta.get_field('payment_date')
        self.assertEqual(field.verbose_name, "Дата оплаты")
        self.assertEqual(field.help_text, "Фактическая дата оплаты")
        self.assertEqual(field.blank, True)
        self.assertEqual(field.null, True)
        self.assertEqual(obj.payment_date, None)

    def test_target_field(self):
        obj = TPayment.objects.get(id=1)
        field = obj._meta.get_field('target')
        self.assertEqual(field.verbose_name, "Цель")
        self.assertEqual(field.max_length, 200)
        self.assertEqual(field.help_text, "Укажите назначение целевого взноса")
        self.assertEqual(obj.target, "Test target")

    def test_amount_field(self):
        obj = TPayment.objects.get(id=1)
        field = obj._meta.get_field('amount')
        self.assertEqual(field.verbose_name, "Сумма")
        self.assertEqual(field.help_text, "Сумма взноса к оплате")
        self.assertEqual(field.max_digits, 7)
        self.assertEqual(field.decimal_places, 2)
        self.assertEqual(obj.amount, 6000)

    def test_land_plot_field(self):
        obj = TPayment.objects.get(id=1)
        plot_obj = LandPlot.objects.get(id=1)
        field = obj._meta.get_field('land_plot')
        #on_delete = obj._meta.get_field('owner').on_delete
        self.assertEqual(field.verbose_name, "Участок")
        self.assertEqual(field.help_text, "Выберите участок")
        self.assertEqual(field.null, True)
        #self.assertEqual(on_delete, models.SET_NULL)
        self.assertEqual(obj.land_plot, plot_obj)

    def test_status_field(self):
        obj = TPayment.objects.get(id=1)
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
        self.assertEquals(TPayment._meta.verbose_name, "целевой взнос")
        self.assertEquals(TPayment._meta.verbose_name_plural, "целевые взносы")
        self.assertEquals(len(TPayment._meta.constraints), 1)
        self.assertEquals(
            TPayment._meta.constraints[0].fields,
            ('target', 'land_plot')
            )
        self.assertEquals(
            TPayment._meta.constraints[0].name,
            'membership_tpayment_target_land_plot_unique_constraint'
            )
   
    def test_str_method(self):
        obj = TPayment.objects.get(id=1)
        object_name = f"{obj.target} {obj.land_plot.plot_number}"
        self.assertEquals(object_name, obj.__str__())
        # or self.assertEquals(object_name, str(obj))
 
    def test_get_absolute_url(self):
        obj = TPayment.objects.get(id=1)
        self.assertEquals(obj.get_absolute_url(), "/data/land-plot-detail/1")
