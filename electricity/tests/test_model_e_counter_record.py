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
            "Внесите показания счетчика (однотарифный)"
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
            "Внесите показания счетчика (тариф день/Т1)"
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
            "Внесите показания счетчика (тариф ночь/Т2)"
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
        self.assertEquals(ECounterRecord._meta.verbose_name, "показания счетчика")
        self.assertEquals(
            ECounterRecord._meta.verbose_name_plural,
            "показания счетчиков"
            )
   
    def test_str_method(self):
        obj = ECounterRecord.objects.get(id=1)
        object_name = f"{obj.rec_date} уч-{obj.land_plot.plot_number}"
        self.assertEquals(object_name, obj.__str__())
        # or self.assertEquals(object_name, str(obj))
 
    def test_get_absolute_url(self):
        obj = ECounterRecord.objects.get(id=1)
        self.assertEquals(obj.get_absolute_url(), "/data/land-plot-detail/1")
