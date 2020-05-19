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
from django.contrib.auth.models import User

class LandPlotModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        ChairMan.objects.create(
            first_name='Иван',
            middle_name='Иванович',
            last_name='Иванов',
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
        )
        LandPlot.objects.create(
            plot_number="10",
            plot_area=6000,
            snt=Snt.objects.get(id=1),
            owner=Owner.objects.get(id=1),
        )
    # Test functions
    def test_plot_number_field(self):
        obj = LandPlot.objects.get(id=1)
        field = obj._meta.get_field('plot_number')
        self.assertEqual(field.verbose_name, "Номер участка")
        self.assertEqual(field.max_length, 10)
        self.assertEqual(field.help_text, "Номер участка")
        self.assertEqual(field.unique, True)
        self.assertEqual(obj.plot_number, "10")

    def test_plot_area_field(self):
        obj = LandPlot.objects.get(id=1)
        field = obj._meta.get_field('plot_area')
        self.assertEqual(field.verbose_name, "Размер участка")
        self.assertEqual(field.help_text, "Единица измерения кв.м")
        self.assertEqual(obj.plot_area, 6000)

    def test_snt_field(self):
        obj = LandPlot.objects.get(id=1)
        snt_obj = Snt.objects.get(id=1)
        field = obj._meta.get_field('snt')
        self.assertEqual(field.verbose_name, "СНТ")
        self.assertEqual(field.help_text, "Расположен в СНТ")
        self.assertEqual(obj.snt, snt_obj)

    def test_owner_field(self):
        obj = LandPlot.objects.get(id=1)
        owner_obj = Owner.objects.get(id=1)
        field = obj._meta.get_field('owner')
        #on_delete = obj._meta.get_field('owner').on_delete
        self.assertEqual(field.verbose_name, "Владелец участка")
        self.assertEqual(field.help_text, "Владелец участка")
        self.assertEqual(field.null, True)
        #self.assertEqual(on_delete, models.SET_NULL)
        self.assertEqual(obj.owner, owner_obj)

    def test_object_name(self):
        obj = LandPlot.objects.get(id=1)
        object_name = f"{obj.plot_number}"
        self.assertEquals(object_name, obj.__str__())
        # or self.assertEquals(object_name, str(obj))
    
    def test_get_absolute_url(self):
        obj = LandPlot.objects.get(id=1)
        self.assertEquals(obj.get_absolute_url(), "/data/land-plot-detail/1")

    def test_verbose_names(self):
        self.assertEquals(LandPlot._meta.verbose_name, "участок")
        self.assertEquals(LandPlot._meta.verbose_name_plural, "участки")
