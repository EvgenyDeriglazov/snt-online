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
        self.assertEqual(obj.s_amount, Decimal('225.00'))

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
        self.assertEqual(obj.sum_total, Decimal('225.00'))

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
        
    def test_calculate(self):
        """Test for calculate() custom method."""
        obj = EPayment.objects.get(id=1)
        # Check for all fields are None
        obj.s_new = None
        obj.s_prev = None
        obj.calculate()
        self.assertEqual(obj.s_cons, None)
        self.assertEqual(obj.t1_cons, None)
        self.assertEqual(obj.t2_cons, None)
        self.assertEqual(obj.s_amount, None)
        self.assertEqual(obj.t1_amount, None)
        self.assertEqual(obj.t2_amount, None)
        self.assertEqual(obj.sum_total, Decimal('0'))
        # Check for single type e_counter
        obj.s_new = 500
        obj.s_prev = 0
        obj.calculate()
        self.assertEqual(obj.s_cons, 500)
        self.assertEqual(obj.s_amount, Decimal('750.00'))
        self.assertEqual(obj.sum_total, Decimal('750.00'))
        # Check for double type e_counter
        obj.s_new = None
        obj.s_prev = None
        obj.t1_new = 100
        obj.t2_new = 100
        obj.t1_prev = 0
        obj.t2_prev = 0
        obj.calculate()
        self.assertEqual(obj.t1_cons, 100)
        self.assertEqual(obj.t2_cons, 100)
        self.assertEqual(obj.t1_amount, Decimal('350.00'))
        self.assertEqual(obj.t2_amount, Decimal('250.00'))
        self.assertEqual(obj.sum_total, Decimal('600.00'))

    def test_save(self):
        """Test for save() custom method."""
        ECounterRecord.objects.filter(id=1).update(rec_date=datetime.date(2019, 1, 1))
        ECounterRecord.objects.create(
            s=500,
            t1=None,
            t2=None,
            land_plot=LandPlot.objects.get(id=1),
            e_counter=ECounter.objects.get(id=1),
            )
        EPayment.objects.create(
            land_plot=LandPlot.objects.get(id=1),
            e_counter_record=ECounterRecord.objects.get(id=2),
            s_new=500,
            s_prev=200,
            )
        obj = EPayment.objects.get(id=2)
        self.assertEqual(obj.s_cons, 300)
        self.assertEqual(obj.t1_cons, None)
        self.assertEqual(obj.t2_cons, None)
        self.assertEqual(obj.s_amount, Decimal('450.00'))
        self.assertEqual(obj.t1_amount, None)
        self.assertEqual(obj.t2_amount, None)
        self.assertEqual(obj.sum_total, Decimal('450.00'))
        # Test protection from calculation and saving for
        # records with status='paid'
        EPayment.objects.filter(id=1).update(
            status='paid',
            )
        obj = EPayment.objects.get(id=1)
        self.assertEqual(obj.s_cons, 150)
        self.assertEqual(obj.status, "paid")
        EPayment.objects.filter(id=1).update(
            s_new=1000,
            )
        obj = EPayment.objects.get(id=1)
        self.assertEqual(obj.s_cons, 150)
        # Test protection from calculation and saving for
        # records with status='payment_confirmed'
        EPayment.objects.filter(id=1).update(
            status='payment_confirmed',
            )
        obj = EPayment.objects.get(id=1)
        self.assertEqual(obj.s_cons, 150)
        self.assertEqual(obj.status, "payment_confirmed")
        EPayment.objects.filter(id=1).update(
            s_new=1000,
            )
        obj = EPayment.objects.get(id=1)
        self.assertEqual(obj.s_cons, 150)
        
    def test_create_qr_text(self):
        """Test for create_qr_text() custom method."""
        obj = EPayment.objects.get(id=1)
        qr_text = 'ST00012|Name=Садоводческое некоммерческое товарищество '
        qr_text += '"Бобровка"|PersonalAcc=01234567898765432101|'
        qr_text += 'BankName=Банк|BIC=123456789|'
        qr_text += 'CorrespAcc=01234567898765432101|INN=0123456789|'
        qr_text += 'LastName=Сергеев|FirstName=Сергей|MiddleName=Сергеевич|'
        qr_text += 'Purpose=Членские взносы за э/энергию, '
        qr_text += 'однотарифный/200-50/150, 150x1.50/225.00. Итого/225.00.|'
        qr_text += 'PayerAddress=участок №10, СНТ "Бобровка"|Sum=22500'
        self.assertEqual(obj.create_qr_text(), qr_text)
    
    def test_paid(self):
        """Test for paid() custom method."""
        EPayment.objects.filter(id=1).update(
            payment_date=None,
            )
        obj = EPayment.objects.get(id=1)
        obj.paid()
        obj = EPayment.objects.get(id=1)
        self.assertEqual(obj.status, 'paid')
        self.assertEqual(obj.payment_date, datetime.date.today())
    
    def test_payment_confirmed(self):
        """Test for payment_confirmed() custom method."""
        EPayment.objects.filter(id=1).update(
            payment_date=None,
            )
        obj = EPayment.objects.get(id=1)
        # Check for status='not_paid'
        obj.payment_confirmed()
        obj = EPayment.objects.get(id=1)
        self.assertEqual(obj.status, 'not_paid')
        self.assertEqual(obj.payment_date, None)
        # Check for status='paid'
        obj.paid()
        obj.payment_confirmed()
        obj = EPayment.objects.get(id=1)
        self.assertEqual(obj.status, 'payment_confirmed')
        self.assertEqual(obj.payment_date, datetime.date.today())
        
        


