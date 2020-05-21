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

class ECounterModelTest(TestCase):
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
    # Test functions
    def test_payment_date_field(self):
        obj = ECounter.objects.get(id=1)
        field = obj._meta.get_field('reg_date')
        self.assertEqual(field.verbose_name, "Дата регистрации")
        self.assertEqual(
            field.help_text,
            "Укажите дату установки нового счетчика"
            + " или приемки к учету в веб приложении уже имеющегося"
            )
        self.assertEqual(obj.reg_date, datetime.date.today())

    def test_model_name_field(self):
        obj = ECounter.objects.get(id=1)
        field = obj._meta.get_field('model_name')
        self.assertEqual(field.verbose_name, "Название модели")
        self.assertEqual(field.max_length, 100)
        self.assertEqual(field.help_text, "Укажите название модели счетчика")
        self.assertEqual(obj.model_name, "test")

    def test_sn_field(self):
        obj = ECounter.objects.get(id=1)
        field = obj._meta.get_field('sn')
        self.assertEqual(field.verbose_name, "Серийный номер")
        self.assertEqual(field.max_length, 50)
        self.assertEqual(field.help_text, "Укажите серийный номер счетчика")
        self.assertEqual(obj.sn, "sn123")

    def test_model_type_field(self):
        obj = ECounter.objects.get(id=1)
        field = obj._meta.get_field('model_type')
        MODEL_TYPE_CHOICES = [
            ('single', 'Однотарифный'),
            ('double', 'Двухтарифный'),
            ]
        self.assertEqual(field.verbose_name, "Тип")
        self.assertEqual(field.max_length, 6)
        self.assertEqual(field.help_text, "Выберите тип счетчика")
        self.assertEqual(field.choices, MODEL_TYPE_CHOICES)
        self.assertEqual(obj.model_type, "single")

    def test_s_field(self):
        obj = ECounter.objects.get(id=1)
        field = obj._meta.get_field('s')
        self.assertEqual(field.verbose_name, "Однотарифный")
        self.assertEqual(
            field.help_text,
            "Показания счетчика на момент установки"
            + "/приемки к учету в веб приложении"
            )
        self.assertEqual(field.blank, True)
        self.assertEqual(field.null, True)
        self.assertEqual(obj.s, 100)

    def test_t1_field(self):
        obj = ECounter.objects.get(id=1)
        field = obj._meta.get_field('t1')
        self.assertEqual(field.verbose_name, "День")
        self.assertEqual(
            field.help_text,
            "Показания счетчика (тариф день/Т1) на момент установки"
            + "/приемки к учету в веб приложении"
            )
        self.assertEqual(field.blank, True)
        self.assertEqual(field.null, True)
        self.assertEqual(obj.t1, None)

    def test_t2_field(self):
        obj = ECounter.objects.get(id=1)
        field = obj._meta.get_field('t2')
        self.assertEqual(field.verbose_name, "Ночь")
        self.assertEqual(
            field.help_text,
            "Показания счетчика (тариф ночь/Т2) на момент установки"
            + "/приемки к учету в веб приложении"
            )
        self.assertEqual(field.blank, True)
        self.assertEqual(field.null, True)
        self.assertEqual(obj.t2, None)

    def test_land_plot_field(self):
        obj = ECounter.objects.get(id=1)
        plot_obj = LandPlot.objects.get(id=1)
        field = obj._meta.get_field('land_plot')
        #on_delete = obj._meta.get_field('owner').on_delete
        self.assertEqual(field.verbose_name, "Участок")
        self.assertEqual(field.help_text, "Выберите участок")
        self.assertEqual(field.null, True)
        #self.assertEqual(on_delete, models.SET_NULL)
        self.assertEqual(obj.land_plot, plot_obj)

    def test_meta_options(self):
        self.assertEquals(ECounter._meta.verbose_name, "счетчик эл.энергии")
        self.assertEquals(
            ECounter._meta.verbose_name_plural,
            "счетчики эл.энергии"
            )
   
    def test_str_method(self):
        obj = ECounter.objects.get(id=1)
        object_name = f"{obj.model_name}"
        self.assertEquals(object_name, obj.__str__())
        # or self.assertEquals(object_name, str(obj))
 
    def test_get_absolute_url(self):
        obj = ECounter.objects.get(id=1)
        self.assertEquals(obj.get_absolute_url(), "/data/land-plot-detail/1")
