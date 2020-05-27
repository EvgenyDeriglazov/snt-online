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
from django.db.models import Q

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
        ERate.objects.create(
            s=1.5,
            t1=3.5,
            t2=2.5,
            snt=Snt.objects.get(id=1),
            )

    # Test functions
    def test_payment_date_field(self):
        obj = ERate.objects.get(id=1)
        field = obj._meta.get_field('date')
        self.assertEqual(field.verbose_name, "Дата")
        self.assertEqual(
            field.help_text,
            "Текущая дата будет использована автоматически"
            + " для нового тарифа за электроэнергию"
            )
        self.assertEqual(obj.date, datetime.date.today())

    def test_s_field(self):
        obj = ERate.objects.get(id=1)
        field = obj._meta.get_field('s')
        self.assertEqual(field.verbose_name, "Однотарифный")
        self.assertEqual(
            field.help_text,
            "Рублей за один кВт/ч для однотарифного э/счетчика"
            )
        self.assertEqual(field.max_digits, 7)
        self.assertEqual(field.decimal_places, 2)
        self.assertEqual(obj.s, 1.5)

    def test_t1_field(self):
        obj = ERate.objects.get(id=1)
        field = obj._meta.get_field('t1')
        self.assertEqual(field.verbose_name, "День")
        self.assertEqual(
            field.help_text,
            "Рублей за один кВт/ч для тарифа Т1 (день)"
            )
        self.assertEqual(field.max_digits, 7)
        self.assertEqual(field.decimal_places, 2)
        self.assertEqual(obj.t1, 3.5)

    def test_t2_field(self):
        obj = ERate.objects.get(id=1)
        field = obj._meta.get_field('t2')
        self.assertEqual(field.verbose_name, "Ночь")
        self.assertEqual(
            field.help_text,
            "Рублей за один кВт/ч для тарифа Т2 (ночь)"
            )
        self.assertEqual(field.max_digits, 7)
        self.assertEqual(field.decimal_places, 2)
        self.assertEqual(obj.t2, 2.5)

    def test_snt_field(self):
        obj = ERate.objects.get(id=1)
        snt_obj = Snt.objects.get(id=1)
        field = obj._meta.get_field('snt')
        #on_delete = obj._meta.get_field('owner').on_delete
        self.assertEqual(field.verbose_name, "СНТ")
        self.assertEqual(
            field.help_text,
            "Выберите СНТ для которого будет применен тариф"
            )
        self.assertEqual(field.null, True)
        #self.assertEqual(on_delete, models.SET_NULL)
        self.assertEqual(obj.snt, snt_obj)

    def test_meta_options(self):
        self.assertEquals(ERate._meta.verbose_name, "тариф за э/энергию")
        self.assertEquals(
            ERate._meta.verbose_name_plural,
            "тарифы за э/энергию"
            )
        self.assertEquals(len(ERate._meta.constraints), 2)
        self.assertEquals(
            ERate._meta.constraints[0].fields,
            ('date',)
            )
        self.assertEquals(
            ERate._meta.constraints[0].name,
            'electricity_erate_date_unique_constraint'
            )
        self.assertEquals(
            ERate._meta.constraints[1].check,
            Q(date__gte=datetime.date.today(),)
            )
        self.assertEquals(
            ERate._meta.constraints[1].name,
            'electricity_erate_date_greater_or_equal_today_constraint'
            )
   
    def test_str_method(self):
        obj = ERate.objects.get(id=1)
        object_name = f"{obj.date}"
        self.assertEquals(object_name, obj.__str__())
        # or self.assertEquals(object_name, str(obj))
 
    def test_get_absolute_url(self):
        obj = ERate.objects.get(id=1)
        self.assertEquals(obj.get_absolute_url(), "/data/land-plot-detail/1")
