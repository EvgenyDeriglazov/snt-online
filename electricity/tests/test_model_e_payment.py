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
from electricity.models import *
from django.contrib.auth.models import User
import datetime
from decimal import *
class EPaymentModelTest(TestCase):
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
        ECounter.objects.create(
            reg_date=datetime.date.today(),
            model_name="test",
            sn="sn123",
            model_type="single",
            s=100,
            t1=None,
            t2=None,
            land_plot=LandPlot.objects.get(id=1),
            )
        ECounterRecord.objects.create(
            s=200,
            t1=None,
            t2=None,
            land_plot=LandPlot.objects.get(id=1),
            e_counter=ECounter.objects.get(id=1),
            )
        ERate.objects.create(
            date=datetime.date.today(),
            s=1.5,
            t1=3.5,
            t2=2.5,
            snt=Snt.objects.get(id=1),
            )
        EPayment.objects.create(
            payment_date=datetime.date.today(),
            s_new=200,
            s_prev=50,
            s_cons=150,
            s_amount=300.55,
            sum_total=300.55,
            status='not_paid',
            land_plot=LandPlot.objects.get(id=1),
            e_counter_record=ECounterRecord.objects.get(id=1),
            )

    # Test functions
    def test_payment_date_field(self):
        obj = EPayment.objects.get(id=1)
        field = obj._meta.get_field('payment_date')
        self.assertEqual(field.verbose_name, "Дата оплаты")
        self.assertEqual(field.help_text, "Фактическая дата оплаты")
        self.assertEqual(field.blank, True)
        self.assertEqual(field.null, True)
        self.assertEqual(obj.payment_date, datetime.date.today())

    def test_s_new_field(self):
        obj = EPayment.objects.get(id=1)
        field = obj._meta.get_field('s_new')
        self.assertEqual(field.verbose_name, "Текущее показание (однотарифный)")
        self.assertEqual(
            field.help_text,
            "Текущее показание э/счетчика (однотарифный) кВт/ч"
            )
        self.assertEqual(field.blank, True)
        self.assertEqual(field.null, True)
        self.assertEqual(obj.s_new, 200)

    def test_t1_new_field(self):
        obj = EPayment.objects.get(id=1)
        field = obj._meta.get_field('t1_new')
        self.assertEqual(field.verbose_name, "Текущее показание (день)")
        self.assertEqual(
            field.help_text,
            "Текущее показание э/счетчика тариф Т1 (день) кВт/ч"
            )
        self.assertEqual(field.blank, True)
        self.assertEqual(field.null, True)
        self.assertEqual(obj.t1_new, None)

    def test_t2_new_field(self):
        obj = EPayment.objects.get(id=1)
        field = obj._meta.get_field('t2_new')
        self.assertEqual(field.verbose_name, "Текущее показание (ночь)")
        self.assertEqual(
            field.help_text,
            "Текущее показание э/счетчика тариф Т2 (ночь) кВт/ч"
            )
        self.assertEqual(field.blank, True)
        self.assertEqual(field.null, True)
        self.assertEqual(obj.t2_new, None)

    def test_s_prev_field(self):
        obj = EPayment.objects.get(id=1)
        field = obj._meta.get_field('s_prev')
        self.assertEqual(field.verbose_name, "Предыдущее показание (однотарифный)")
        self.assertEqual(
            field.help_text,
            "Предыдущее показание э/счетчика (однотарифный) кВт/ч"
            )
        self.assertEqual(field.blank, True)
        self.assertEqual(field.null, True)
        self.assertEqual(obj.s_prev, 50)

    def test_t1_prev_field(self):
        obj = EPayment.objects.get(id=1)
        field = obj._meta.get_field('t1_prev')
        self.assertEqual(field.verbose_name, "Предыдущее показание (день)")
        self.assertEqual(
            field.help_text,
            "Предыдущее показание э/счетчика тариф Т1 (день) кВт/ч"
            )
        self.assertEqual(field.blank, True)
        self.assertEqual(field.null, True)
        self.assertEqual(obj.t1_prev, None)

    def test_t2_prev_field(self):
        obj = EPayment.objects.get(id=1)
        field = obj._meta.get_field('t2_prev')
        self.assertEqual(field.verbose_name, "Предыдущее показание (ночь)")
        self.assertEqual(
            field.help_text,
            "Предыдущее показание э/счетчика тариф Т2 (ночь) кВт/ч"
            )
        self.assertEqual(field.blank, True)
        self.assertEqual(field.null, True)
        self.assertEqual(obj.t2_prev, None)

    def test_s_cons_field(self):
        obj = EPayment.objects.get(id=1)
        field = obj._meta.get_field('s_cons')
        self.assertEqual(field.verbose_name, "Расход (однотарифный)")
        self.assertEqual(field.help_text, "Расход кВт/ч (однотарифный)")
        self.assertEqual(field.blank, True)
        self.assertEqual(field.null, True)
        self.assertEqual(obj.s_cons, 150)

    def test_t1_cons_field(self):
        obj = EPayment.objects.get(id=1)
        field = obj._meta.get_field('t1_cons')
        self.assertEqual(field.verbose_name, "Расход (день)")
        self.assertEqual(field.help_text, "Расход кВт/ч тариф Т1 (день)")
        self.assertEqual(field.blank, True)
        self.assertEqual(field.null, True)
        self.assertEqual(obj.t1_cons, None)

    def test_t2_cons_field(self):
        obj = EPayment.objects.get(id=1)
        field = obj._meta.get_field('t2_cons')
        self.assertEqual(field.verbose_name, "Расход (ночь)")
        self.assertEqual(field.help_text, "Расход кВт/ч тариф Т2 (ночь)")
        self.assertEqual(field.blank, True)
        self.assertEqual(field.null, True)
        self.assertEqual(obj.t2_cons, None)

    def test_s_amount_field(self):
        obj = EPayment.objects.get(id=1)
        field = obj._meta.get_field('s_amount')
        self.assertEqual(field.verbose_name, "Сумма (однотарифный)")
        self.assertEqual(field.help_text, "Сумма (однотарифный)")
        self.assertEqual(field.max_digits, 7)
        self.assertEqual(field.decimal_places, 2)
        self.assertEqual(field.blank, True)
        self.assertEqual(field.null, True)
        self.assertEqual(obj.s_amount, Decimal('300.55'))

    def test_t1_amount_field(self):
        obj = EPayment.objects.get(id=1)
        field = obj._meta.get_field('t1_amount')
        self.assertEqual(field.verbose_name, "Сумма (день)")
        self.assertEqual(field.help_text, "Сумма тариф Т1 (день)")
        self.assertEqual(field.max_digits, 7)
        self.assertEqual(field.decimal_places, 2)
        self.assertEqual(field.blank, True)
        self.assertEqual(field.null, True)
        self.assertEqual(obj.t1_amount, None)

    def test_t2_amount_field(self):
        obj = EPayment.objects.get(id=1)
        field = obj._meta.get_field('t2_amount')
        self.assertEqual(field.verbose_name, "Сумма (ночь)")
        self.assertEqual(field.help_text, "Сумма тариф Т2 (ночь)")
        self.assertEqual(field.max_digits, 7)
        self.assertEqual(field.decimal_places, 2)
        self.assertEqual(field.blank, True)
        self.assertEqual(field.null, True)
        self.assertEqual(obj.t2_amount, None)

    def test_sum_total_field(self):
        obj = EPayment.objects.get(id=1)
        field = obj._meta.get_field('sum_total')
        self.assertEqual(field.verbose_name, "Итого")
        self.assertEqual(field.help_text, "Итого")
        self.assertEqual(field.max_digits, 8)
        self.assertEqual(field.decimal_places, 2)
        self.assertEqual(obj.sum_total, Decimal('300.55'))

    def test_status_field(self):
        obj = EPayment.objects.get(id=1)
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

    def test_land_plot_field(self):
        obj = EPayment.objects.get(id=1)
        plot_obj = LandPlot.objects.get(id=1)
        field = obj._meta.get_field('land_plot')
        #on_delete = obj._meta.get_field('owner').on_delete
        self.assertEqual(field.verbose_name, "Участок")
        self.assertEqual(field.help_text, "Выберите участок")
        self.assertEqual(field.null, True)
        #self.assertEqual(on_delete, models.SET_NULL)
        self.assertEqual(obj.land_plot, plot_obj)

    def test_e_counter_record_field(self):
        obj = EPayment.objects.get(id=1)
        record_obj = ECounterRecord.objects.get(id=1)
        field = obj._meta.get_field('e_counter_record')
        #on_delete = obj._meta.get_field('owner').on_delete
        self.assertEqual(field.verbose_name, "Запись показаний э/счетчика")
        self.assertEqual(field.help_text, "Выберите запись показаний э/счетчика")
        self.assertEqual(field.null, True)
        #self.assertEqual(on_delete, models.SET_NULL)
        self.assertEqual(obj.e_counter_record, record_obj)
   
    def test_meta_options(self):
        self.assertEquals(EPayment._meta.verbose_name, "взнос за э/энергию")
        self.assertEquals(EPayment._meta.verbose_name_plural, "взонсы за э/энергию")

    def test_str_method(self):
        obj = EPayment.objects.get(id=1)
        object_name = f"{obj.payment_date}-{obj.land_plot.plot_number}"
        self.assertEquals(object_name, obj.__str__())
        # or self.assertEquals(object_name, str(obj))
 
    def test_get_absolute_url(self):
        obj = EPayment.objects.get(id=1)
        self.assertEquals(obj.get_absolute_url(), "/data/land-plot-detail/1")
