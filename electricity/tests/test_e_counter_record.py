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

class ECounterRecordModelTest(TestCase):
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
        ERate.objects.create(
            date=datetime.date.today(),
            s=1.5,
            t1=3.5,
            t2=2.5,
            snt=Snt.objects.get(id=1),
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

    # Test functions
    def test_payment_date_field(self):
        obj = ECounterRecord.objects.get(id=1)
        field = obj._meta.get_field('rec_date')
        self.assertEqual(field.verbose_name, "Дата показаний")
        self.assertEqual(
            field.help_text,
            "Текущая дата будет использована автоматически"
            + " для сохранения показаний"
            )
        self.assertEqual(obj.rec_date, datetime.date.today())

    def test_s_field(self):
        obj = ECounterRecord.objects.get(id=1)
        field = obj._meta.get_field('s')
        self.assertEqual(field.verbose_name, "Однотарифный")
        self.assertEqual(
            field.help_text,
            "Внесите показания э/счетчика (однотарифный)"
            )
        self.assertEqual(field.blank, True)
        self.assertEqual(field.null, True)
        self.assertEqual(obj.s, 200)

    def test_t1_field(self):
        obj = ECounterRecord.objects.get(id=1)
        field = obj._meta.get_field('t1')
        self.assertEqual(field.verbose_name, "День")
        self.assertEqual(
            field.help_text,
            "Внесите показания э/счетчика тариф Т1 (день)"
            )
        self.assertEqual(field.blank, True)
        self.assertEqual(field.null, True)
        self.assertEqual(obj.t1, None)

    def test_t2_field(self):
        obj = ECounterRecord.objects.get(id=1)
        field = obj._meta.get_field('t2')
        self.assertEqual(field.verbose_name, "Ночь")
        self.assertEqual(
            field.help_text,
            "Внесите показания э/счетчика тариф Т2 (ночь)"
            )
        self.assertEqual(field.blank, True)
        self.assertEqual(field.null, True)
        self.assertEqual(obj.t2, None)

    def test_land_plot_field(self):
        obj = ECounterRecord.objects.get(id=1)
        plot_obj = LandPlot.objects.get(id=1)
        field = obj._meta.get_field('land_plot')
        #on_delete = obj._meta.get_field('owner').on_delete
        self.assertEqual(field.verbose_name, "Участок")
        self.assertEqual(field.help_text, "Выберите участок")
        self.assertEqual(field.null, True)
        #self.assertEqual(on_delete, models.SET_NULL)
        self.assertEqual(obj.land_plot, plot_obj)

    def test_e_counter_field(self):
        obj = ECounterRecord.objects.get(id=1)
        e_counter_obj = ECounter.objects.get(id=1)
        field = obj._meta.get_field('e_counter')
        #on_delete = obj._meta.get_field('owner').on_delete
        self.assertEqual(field.verbose_name, "Счетчик")
        self.assertEqual(field.help_text, "Выберите счетчик")
        self.assertEqual(field.null, True)
        #self.assertEqual(on_delete, models.SET_NULL)
        self.assertEqual(obj.e_counter, e_counter_obj)

    def test_meta_options(self):
        self.assertEqual(ECounterRecord._meta.verbose_name, "показания э/счетчика")
        self.assertEqual(
            ECounterRecord._meta.verbose_name_plural,
            "показания э/счетчиков"
            )
        self.assertEqual(len(ECounterRecord._meta.constraints), 1)
        self.assertEqual(
            ECounterRecord._meta.constraints[0].fields,
            ('rec_date', 'land_plot','e_counter',)
            )
        self.assertEqual(
            ECounterRecord._meta.constraints[0].name,
            'electricity_ecounterrecord_rec_date_land_plot_e_counter'
                + '_unique_constraint'
            )
   
    def test_str_method(self):
        obj = ECounterRecord.objects.get(id=1)
        object_name = f"{obj.rec_date} уч-{obj.land_plot.plot_number}"
        self.assertEqual(object_name, obj.__str__())
        # or self.assertEqual(object_name, str(obj))
 
    def test_get_absolute_url(self):
        obj = ECounterRecord.objects.get(id=1)
        self.assertEqual(obj.get_absolute_url(), None)

    def test_records_exist(self):
        """Test records_exist() model custom method."""
        obj = ECounterRecord.objects.get(id=1)
        self.assertEqual(obj.records_exist(), True)
        ECounterRecord.objects.all().delete()
        self.assertEqual(obj.records_exist(), False)

    def test_e_counter_single_type_fields_ok(self):
        """Tests e_counter_single_type_fields_ok() model custom method."""
        obj = ECounterRecord.objects.get(id=1)
        self.assertEqual(obj.e_counter_single_type_fields_ok(), True)
        obj.s = None
        obj.t1 = 5
        obj.t2 = 5
        self.assertEqual(obj.e_counter_single_type_fields_ok(), False)

    def test_e_counter_double_type_fields_ok(self):
        """Tests e_counter_double_type_fields_ok() model custom method."""
        obj = ECounterRecord.objects.get(id=1)
        self.assertEqual(obj.e_counter_double_type_fields_ok(), False)
        obj.s = None
        obj.t1 = 5
        obj.t2 = 5
        self.assertEqual(obj.e_counter_double_type_fields_ok(), True)

    def test_get_latest_record(self):
        """get_latest_record() with/without record."""
        ECounterRecord.objects.filter(id=1).update(
            rec_date=datetime.date.today() - datetime.timedelta(days=5)
            )
        ECounterRecord.objects.create(
            s=400,
            t1=None,
            t2=None,
            land_plot=LandPlot.objects.get(id=1),
            e_counter=ECounter.objects.get(id=1),
            )
        obj = ECounterRecord.objects.get(id=1)
        obj_latest = ECounterRecord.objects.get(id=2)
        self.assertEqual(obj.get_latest_record(), obj_latest)
        ECounterRecord.objects.all().delete()
        self.assertEqual(obj.get_latest_record(), None)
    
    def test_sinlge_error_message(self):
        """single_error_message() custom method."""
        obj = ECounterRecord.objects.get(id=1)
        self.assertEqual(
            obj.single_error_message(10, 12),
            "Новое показание 10 должно быть больше предыдущего 12"
            )
        
    def test_double_error_message(self):
        """double_error_message() custom method."""
        obj = ECounterRecord.objects.get(id=1)
        self.assertEqual(
            obj.double_error_message(1, 2, 5, 8),
            "Новые показания должны быть больше старых. День: 1 > 2. Ночь: 5 > 8."
            )
 
    def test_check_vs_latest_record_no_record_single_type(self):
        """check_vs_latest_record() for single type with/without record."""
        # Prepare objects in db
        ECounterRecord.objects.filter(id=1).update(
            rec_date=datetime.date.today() - datetime.timedelta(days=5)
            )
        ECounterRecord.objects.create(
            s=400,
            t1=None,
            t2=None,
            land_plot=LandPlot.objects.get(id=1),
            e_counter=ECounter.objects.get(id=1),
            )
        # Check
        obj = ECounterRecord.objects.get(id=2)
        obj_latest = ECounterRecord.objects.get(id=1)
        self.assertEqual(obj.check_vs_latest_record(obj_latest, "single"), True)
        self.assertEqual(obj.check_vs_latest_record(None, "single"), True)
    
    def test_check_vs_latest_record_no_record_double_type(self):
        """check_vs_latest_record() for double type with/without record."""
        # Prepare objects in db
        ECounter.objects.filter(id=1).update(
            model_type="double",
            s=None,
            t1=0,
            t2=0,
            )
        ECounterRecord.objects.filter(id=1).update(
            rec_date=datetime.date.today() - datetime.timedelta(days=5),
            s=None,
            t1=100,
            t2=100,
            )
        ECounterRecord.objects.create(
            s=None,
            t1=200,
            t2=200,
            land_plot=LandPlot.objects.get(id=1),
            e_counter=ECounter.objects.get(id=1),
            )
        # Check vs latest object in db (double type)
        obj = ECounterRecord.objects.get(id=2)
        obj_latest = ECounterRecord.objects.get(id=1)
        self.assertEqual(obj.check_vs_latest_record(obj_latest, "double"), True)
        self.assertEqual(obj.check_vs_latest_record(None, "double"), True)

    def test_check_vs_latest_record_no_record_single_type_error(self):
        """check_vs_latest_record(None, "single")."""
        obj = ECounterRecord.objects.get(id=1)
        obj.s = 0
        self.assertEqual(obj.check_vs_latest_record(None, "single"), False)
 
    def test_check_vs_latest_record_no_record_double_type_error(self):
        """check_vs_latest_record(None, "double")"""
        obj = ECounterRecord.objects.get(id=1)
        ECounter.objects.filter(id=1).update(
            model_type="double",
            s=None,
            t1=0,
            t2=0,
            )
        obj.s = None
        obj.t1 = 0
        obj.t2 = 0
        self.assertEqual(obj.check_vs_latest_record(None, "double"), False)
 
    def test_check_vs_latest_record_single_type_error(self):
        """check_vs_latest_record() for single type, ValidationError."""
        ECounterRecord.objects.filter(id=1).update(
            rec_date=datetime.date.today() - datetime.timedelta(days=5),
            )
        obj = ECounterRecord.objects.get(id=1)
        ECounterRecord.objects.create(
            s=300,
            t1=None,
            t2=None,
            land_plot=LandPlot.objects.get(id=1),
            e_counter=ECounter.objects.get(id=1),
            )
        obj_2 = ECounterRecord.objects.get(id=2)
        self.assertEqual(obj_2.check_vs_latest_record(obj, "single"), True)
        obj_2.s = 0
        self.assertEqual(obj_2.check_vs_latest_record(obj, "single"), False)

    def test_check_vs_latest_record_double_type_error(self):
        """check_vs_latest_record(error_obj, "double")"""
        ECounter.objects.filter(id=1).update(
            model_type="double",
            s=None,
            t1=0,
            t2=0,
            )
        ECounterRecord.objects.filter(id=1).update(
            rec_date=datetime.date.today() - datetime.timedelta(days=5),
            s=None,
            t1=10,
            t2=10,
            )
        ECounterRecord.objects.create(
            s=None,
            t1=20,
            t2=20,
            land_plot=LandPlot.objects.get(id=1),
            e_counter=ECounter.objects.get(id=1),
            )
        obj = ECounterRecord.objects.get(id=1)
        obj_2 = ECounterRecord.objects.get(id=2)
        obj_2.t1 = 0
        obj_2.t2 = 0
        self.assertEqual(obj_2.check_vs_latest_record(obj, "double"), False)
        
    def test_save_no_records_single_type_validation_error(self):
        """Test for save() with single type model, incorrect fields 
        and no records."""
        ECounterRecord.objects.all().delete()
        with self.assertRaises(Http404):
            ECounterRecord.objects.create(
                s = 0,
                t1 = None,
                t2 = None,
                land_plot = LandPlot.objects.get(id=1),
                e_counter = ECounter.objects.get(id=1),
                )
        with self.assertRaisesRegex(Http404, ''):
            ECounterRecord.objects.create(
                s = 0,
                t1 = None,
                t2 = None,
                land_plot = LandPlot.objects.get(id=1),
                e_counter = ECounter.objects.get(id=1),
                )

    def test_save_no_records_double_type_validation_error(self):
        """Test for save() with single type model, incorrect fields 
        and no records."""
        ECounterRecord.objects.all().delete()
        ECounter.objects.filter(id=1).update(
            model_type="double",
            s=None,
            t1=100,
            t2=100,
            )
        with self.assertRaises(Http404):
            ECounterRecord.objects.create(
                s = None,
                t1 = 0,
                t2 = 0,
                land_plot = LandPlot.objects.get(id=1),
                e_counter = ECounter.objects.get(id=1),
                )
        with self.assertRaisesRegex(Http404, ''):
            ECounterRecord.objects.create(
                s = None,
                t1 = 0,
                t2 = 0,
                land_plot = LandPlot.objects.get(id=1),
                e_counter = ECounter.objects.get(id=1),
                )
 
    def test_save_single_type_validation_error(self):
        """Test for save() with single type model and incorrect fields."""
        with self.assertRaises(Http404):
            ECounterRecord.objects.create(
                s = 0,
                t1 = None,
                t2 = None,
                land_plot = LandPlot.objects.get(id=1),
                e_counter = ECounter.objects.get(id=1),
                )
        with self.assertRaisesRegex(Http404, ''):
            ECounterRecord.objects.create(
                s = 0,
                t1 = None,
                t2 = None,
                land_plot = LandPlot.objects.get(id=1),
                e_counter = ECounter.objects.get(id=1),
                )

    def test_save_double_type_validation_error(self):
        """Test for save() with double type model and incorrect fields."""
        ECounter.objects.filter(id=1).update(
            model_type="double",
            s=None,
            t1=100,
            t2=100,
            )
        ECounterRecord.objects.filter(id=1).update(
            #rec_date=datetime.date.today() - datetime.timedelta(days=5),
            s=None,
            t1=100,
            t2=100,
            )
        with self.assertRaises(Http404):
            ECounterRecord.objects.create(
                s = None,
                t1 = 0,
                t2 = 0,
                land_plot = LandPlot.objects.get(id=1),
                e_counter = ECounter.objects.get(id=1),
                )
        with self.assertRaisesRegex(Http404, ''):
            ECounterRecord.objects.create(
                s = None,
                t1 = 0,
                t2 = 0,
                land_plot = LandPlot.objects.get(id=1),
                e_counter = ECounter.objects.get(id=1),
                )

    def test_save_single_model_type_with_error_fixing(self):
        """Test for save() with single model and fields error fixing."""
        ECounterRecord.objects.filter(id=1).update(
            rec_date=datetime.date.today() - datetime.timedelta(days=5),
            )
        ECounterRecord.objects.create(
            s=400,
            t1=100,
            t2=100,
            land_plot=LandPlot.objects.get(id=1),
            e_counter=ECounter.objects.get(id=1),
            )
        all_obj = ECounterRecord.objects.all()
        self.assertEqual(len(all_obj), 2)
        self.assertEqual(all_obj[1].s, 400)
        self.assertEqual(all_obj[1].t1, None)
        self.assertEqual(all_obj[1].t2, None)

    def test_save_double_model_type_with_error_fixing(self):
        """Test for save() with double model and fields error fixing."""
        ECounter.objects.filter(id=1).update(
            model_type="double",
            s=None,
            t1=0,
            t2=0,
            )
        ECounterRecord.objects.filter(id=1).update(
            rec_date=datetime.date.today() - datetime.timedelta(days=5),
            s=None,
            t1=100,
            t2=100,
            )
        ECounterRecord.objects.create(
            s=100,
            t1=200,
            t2=200,
            land_plot=LandPlot.objects.get(id=1),
            e_counter=ECounter.objects.get(id=1),
            )
        all_obj = ECounterRecord.objects.all()
        self.assertEqual(len(all_obj), 2)
        self.assertEqual(all_obj[1].s, None)
        self.assertEqual(all_obj[1].t1, 200)
        self.assertEqual(all_obj[1].t2, 200)
    
    def test_save_no_records_exist_single_type_model(self):
        """Test for save() with no records in db and single type model."""
        ECounterRecord.objects.all().delete()
        self.assertEqual(len(ECounterRecord.objects.all()), 0)
        ECounterRecord.objects.create(
            s=200,
            t1=None,
            t2=None,
            land_plot=LandPlot.objects.get(id=1),
            e_counter=ECounter.objects.get(id=1),
            )
        self.assertEqual(len(ECounterRecord.objects.all()), 1)
    
    def test_save_no_records_exist_double_type_model(self):
        """Test for save() with no records in db and double type model."""
        ECounterRecord.objects.all().delete()
        self.assertEqual(len(ECounterRecord.objects.all()), 0)
        ECounter.objects.update(
            model_type="double",
            s=None,
            t1=0,
            t2=0,
            )
        ECounterRecord.objects.create(
            s=None,
            t1=100,
            t2=10,
            land_plot=LandPlot.objects.get(id=1),
            e_counter=ECounter.objects.get(id=1),
            )
        self.assertEqual(len(ECounterRecord.objects.all()), 1)

    def test_no_e_payment(self):
        """Test for no_e_payment() method."""
        obj = ECounterRecord.objects.get(id=1)
        self.assertEqual(obj.no_e_payment(), True)
        EPayment.objects.create(
            land_plot=obj.land_plot,
            e_counter_record=obj,
            s_new = 100,
            s_prev = 0,
            )
        self.assertEqual(obj.no_e_payment(), False)
    
    def test_e_payments_exist(self):
        """Test e_payments_exist() method."""
        obj = ECounterRecord.objects.get(id=1)
        self.assertEqual(obj.e_payments_exist(), False)
        EPayment.objects.create(
            land_plot=obj.land_plot,
            e_counter_record=ECounterRecord.objects.get(id=1),
            s_new = 100,
            s_prev = 0,
            )
        self.assertEqual(obj.e_payments_exist(), True)
 
    def test_no_unpaid_and_paid_payments(self):
        """Test for no_unpaid_and_paid_payments() method."""
        obj = ECounterRecord.objects.get(id=1)
        self.assertEqual(obj.no_unpaid_and_paid_payments(), True)
        EPayment.objects.create(
            land_plot=obj.land_plot,
            e_counter_record=ECounterRecord.objects.get(id=1),
            s_new = 100,
            s_prev = 0,
            )
        self.assertEqual(obj.no_unpaid_and_paid_payments(), False)
        EPayment.objects.filter(id=1).update(status='payment_confirmed')
        self.assertEqual(obj.no_unpaid_and_paid_payments(), True)
        
    def test_last_payment_confirmed_e_counter_record(self):
        """Test for last_payment_confirmed_e_counter_record() method."""
        ECounterRecord.objects.filter(id=1).update(rec_date=datetime.date(2019, 1, 1))
        obj = ECounterRecord.objects.get(id=1)
        EPayment.objects.create(
            payment_date=datetime.date(2019, 1, 1),
            s_new=obj.s,
            s_prev=100,
            land_plot=obj.land_plot,
            e_counter_record=obj,
            )
        EPayment.objects.filter(id=1).update(status="payment_confirmed")
        ECounterRecord.objects.create(
            s=300,
            land_plot=LandPlot.objects.get(id=1),
            e_counter=ECounter.objects.get(id=1),
            )
        last_obj = ECounterRecord.objects.get(id=2)
        EPayment.objects.create(
            payment_date=datetime.date.today(),
            s_new=last_obj.s,
            s_prev=obj.s,
            land_plot=obj.land_plot,
            e_counter_record=last_obj,
            )
        EPayment.objects.filter(id=2).update(status="payment_confirmed")
        self.assertEqual(obj.last_payment_confirmed_e_counter_record(), last_obj)
        EPayment.objects.filter(id=2).update(status="unpaid")
        self.assertEqual(obj.last_payment_confirmed_e_counter_record(), obj)
    
    def test_create_e_payment_single_type(self):
        """Test create_e_payment() - full logic single type."""
        # Test first if/else results and second else result
        obj = ECounterRecord.objects.get(id=1)
        obj.create_e_payment()
        with self.assertRaises(ValidationError):
            obj.create_e_payment()
        with self.assertRaisesRegex(ValidationError, ''):
            obj.create_e_payment()
        all_payments = EPayment.objects.all()
        self.assertEqual(len(all_payments), 1)
        self.assertEqual(all_payments[0].s_new, 200)
        self.assertEqual(all_payments[0].s_prev, 100)
        self.assertEqual(all_payments[0].t1_new, None)
        self.assertEqual(all_payments[0].t2_new, None)
        self.assertEqual(all_payments[0].t1_prev, None)
        self.assertEqual(all_payments[0].t2_prev, None)
        self.assertEqual(all_payments[0].s_cons, 100)
        self.assertEqual(all_payments[0].t1_cons, None)
        self.assertEqual(all_payments[0].t2_cons, None)
        self.assertEqual(all_payments[0].s_amount, Decimal('150.00'))
        self.assertEqual(all_payments[0].t1_amount, None)
        self.assertEqual(all_payments[0].t2_amount, None)
        self.assertEqual(all_payments[0].sum_total, Decimal('150.00'))
        self.assertEqual(all_payments[0].land_plot, obj.land_plot)
        self.assertEqual(all_payments[0].e_counter_record, obj)
        # Test second if and third else results
        ECounterRecord.objects.filter(id=1).update(
            rec_date=datetime.date(2019, 1, 1),
            )
        ECounterRecord.objects.create(
            s=300,
            t1=None,
            t2=None,
            land_plot=LandPlot.objects.get(id=1),
            e_counter=ECounter.objects.get(id=1),
            )
        second_obj = ECounterRecord.objects.get(id=2)
        with self.assertRaises(ValidationError):
            second_obj.create_e_payment()
        with self.assertRaisesRegex(ValidationError, ''):
            second_obj.create_e_payment()
        # Test third if result
        EPayment.objects.filter(id=1).update(
            status="payment_confirmed",
            )
        ECounterRecord.objects.filter(id=2).update(
            rec_date=datetime.date(2019, 2, 1),
            )
        ECounterRecord.objects.create(
            s=400,
            t1=None,
            t2=None,
            land_plot=LandPlot.objects.get(id=1),
            e_counter=ECounter.objects.get(id=1),
            )
        third_obj = ECounterRecord.objects.get(id=3)
        third_obj.create_e_payment()
        all_payments = EPayment.objects.all()
        all_obj = ECounterRecord.objects.all()
        self.assertEqual(len(all_payments), 2)
        self.assertEqual(len(all_obj), 2)
        self.assertEqual(all_payments[1].e_counter_record, all_obj[1])
        self.assertEqual(all_payments[1].s_new, 400)
        self.assertEqual(all_payments[1].s_prev, 200)
        self.assertEqual(all_payments[1].t1_new, None)
        self.assertEqual(all_payments[1].t2_new, None)
        self.assertEqual(all_payments[1].t1_prev, None)
        self.assertEqual(all_payments[1].t2_prev, None)
        self.assertEqual(all_payments[1].s_cons, 200)
        self.assertEqual(all_payments[1].t1_cons, None)
        self.assertEqual(all_payments[1].t2_cons, None)
        self.assertEqual(all_payments[1].s_amount, Decimal('300.00'))
        self.assertEqual(all_payments[1].t1_amount, None)
        self.assertEqual(all_payments[1].t2_amount, None)
        self.assertEqual(all_payments[1].sum_total, Decimal('300.00'))
 
    def test_create_e_payment_double_type(self):
        """Test create_e_payment() - full logic double type."""
        # Test first if/else results and second else result
        ECounter.objects.filter(id=1).update(
            model_type="double",
            s=None,
            t1=100,
            t2=100,
            )
        ECounterRecord.objects.filter(id=1).update(
            s=None,
            t1=200,
            t2=200,
            )
        obj = ECounterRecord.objects.get(id=1)
        obj.create_e_payment()
        with self.assertRaises(ValidationError):
            obj.create_e_payment()
        with self.assertRaisesRegex(ValidationError, ''):
            obj.create_e_payment()
        all_payments = EPayment.objects.all()
        self.assertEqual(len(all_payments), 1)
        self.assertEqual(all_payments[0].s_new, None)
        self.assertEqual(all_payments[0].s_prev, None)
        self.assertEqual(all_payments[0].t1_new, 200)
        self.assertEqual(all_payments[0].t2_new, 200)
        self.assertEqual(all_payments[0].t1_prev, 100)
        self.assertEqual(all_payments[0].t2_prev, 100)
        self.assertEqual(all_payments[0].s_cons, None)
        self.assertEqual(all_payments[0].t1_cons, 100)
        self.assertEqual(all_payments[0].t2_cons, 100)
        self.assertEqual(all_payments[0].s_amount, None)
        self.assertEqual(all_payments[0].t1_amount, Decimal('350.00'))
        self.assertEqual(all_payments[0].t2_amount, Decimal('250.00'))
        self.assertEqual(all_payments[0].sum_total, Decimal('600.00'))
        self.assertEqual(all_payments[0].land_plot, obj.land_plot)
        self.assertEqual(all_payments[0].e_counter_record, obj)
        # Test second if and third else results
        ECounterRecord.objects.filter(id=1).update(
            rec_date=datetime.date(2019, 1, 1),
            )
        ECounterRecord.objects.create(
            s=None,
            t1=300,
            t2=300,
            land_plot=LandPlot.objects.get(id=1),
            e_counter=ECounter.objects.get(id=1),
            )
        second_obj = ECounterRecord.objects.get(id=2)
        with self.assertRaises(ValidationError):
            second_obj.create_e_payment()
        with self.assertRaisesRegex(ValidationError, ''):
            second_obj.create_e_payment()
        # Test third if result
        EPayment.objects.filter(id=1).update(
            status="payment_confirmed",
            )
        ECounterRecord.objects.filter(id=2).update(
            rec_date=datetime.date(2019, 2, 1),
            )
        ECounterRecord.objects.create(
            s=None,
            t1=400,
            t2=400,
            land_plot=LandPlot.objects.get(id=1),
            e_counter=ECounter.objects.get(id=1),
            )
        third_obj = ECounterRecord.objects.get(id=3)
        third_obj.create_e_payment()
        all_payments = EPayment.objects.all()
        all_obj = ECounterRecord.objects.all()
        self.assertEqual(len(all_payments), 2)
        self.assertEqual(len(all_obj), 2)
        self.assertEqual(all_payments[1].land_plot, all_obj[1].land_plot)
        self.assertEqual(all_payments[1].e_counter_record, all_obj[1])
        self.assertEqual(all_payments[1].s_new, None)
        self.assertEqual(all_payments[1].s_prev, None)
        self.assertEqual(all_payments[1].t1_new, 400)
        self.assertEqual(all_payments[1].t2_new, 400)
        self.assertEqual(all_payments[1].t1_prev, 200)
        self.assertEqual(all_payments[1].t2_prev, 200)
        self.assertEqual(all_payments[1].s_cons, None)
        self.assertEqual(all_payments[1].t1_cons, 200)
        self.assertEqual(all_payments[1].t2_cons, 200)
        self.assertEqual(all_payments[1].s_amount, None)
        self.assertEqual(all_payments[1].t1_amount, Decimal('700.00'))
        self.assertEqual(all_payments[1].t2_amount, Decimal('500.00'))
        self.assertEqual(all_payments[1].sum_total, Decimal('1200.00'))
 
