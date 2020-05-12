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
from data.models import *
from datetime import date
from decimal import *

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
            status='c',
            start_owner_date=date(2020, 1, 1),
            end_owner_date=None,
        )
        ElectricMeter.objects.create(
            model="НЕВА",
            serial_number="123456789",
            model_type="T1",
            acceptance_date=None,
        )
        LandPlot.objects.create(
            plot_number="10",
            plot_area=6000,
            snt=Snt.objects.get(id=1),
            owner=Owner.objects.get(id=1),
            electric_meter=ElectricMeter.objects.get(id=1),
        )
    # Test functions
    def test_plot_number_field(self):
        l_p = LandPlot.objects.get(id=1)
        field_label = l_p._meta.get_field('plot_number').verbose_name
        max_length = l_p._meta.get_field('plot_number').max_length
        help_text = l_p._meta.get_field('plot_number').help_text 
        unique_prop = l_p._meta.get_field('plot_number').unique
        self.assertEqual(field_label, "Номер участка")
        self.assertEqual(max_length, 10)
        self.assertEqual(help_text, "Номер участка")
        self.assertEqual(unique_prop, True)
        self.assertEqual(l_p.plot_number, "10")

    def test_plot_area_field(self):
        l_p = LandPlot.objects.get(id=1)
        field_label = l_p._meta.get_field('plot_area').verbose_name
        help_text = l_p._meta.get_field('plot_area').help_text 
        self.assertEqual(field_label, "Размер участка")
        self.assertEqual(help_text, "Единица измерения кв.м")
        self.assertEqual(l_p.plot_area, 6000)

    def test_snt_field(self):
        lp_obj = LandPlot.objects.get(id=1)
        snt_obj = Snt.objects.get(id=1)
        field_label = lp_obj._meta.get_field('snt').verbose_name
        help_text = lp_obj._meta.get_field('snt').help_text 
        self.assertEqual(field_label, "СНТ")
        self.assertEqual(help_text, "Расположен в СНТ")
        self.assertEqual(lp_obj.snt, snt_obj)

    def test_owner_field(self):
        lp_obj = LandPlot.objects.get(id=1)
        owner_obj = Owner.objects.get(id=1)
        field_label = lp_obj._meta.get_field('owner').verbose_name
        help_text = lp_obj._meta.get_field('owner').help_text
        is_null = lp_obj._meta.get_field('owner').null
        #on_delete = lp_obj._meta.get_field('owner').on_delete
        self.assertEqual(field_label, "владелец участка")
        self.assertEqual(help_text, "Владелец участка")
        self.assertEqual(is_null, True)
        #self.assertEqual(on_delete, models.SET_NULL)
        self.assertEqual(lp_obj.owner, owner_obj)

    def test_electric_meter_field(self):
        lp_obj = LandPlot.objects.get(id=1)
        em_obj = ElectricMeter.objects.get(id=1)
        field_label = lp_obj._meta.get_field('electric_meter').verbose_name
        help_text = lp_obj._meta.get_field('electric_meter').help_text
        is_null = lp_obj._meta.get_field('electric_meter').null
        self.assertEqual(field_label, "Счетчик")
        self.assertEqual(help_text, "Данные прибора учета электроэнергии")
        self.assertEqual(is_null, True)
        self.assertEqual(lp_obj.electric_meter, em_obj)
        
    def test_object_name(self):
        lp_obj = LandPlot.objects.get(id=1)
        object_name = f'{lp_obj.plot_number}'
        self.assertEquals(object_name, lp_obj.__str__())
        # or self.assertEquals(object_name, str(lp_obj))
    
    def test_get_absolute_url(self):
        lp_obj = LandPlot.objects.get(id=1)
        self.assertEquals(lp_obj.get_absolute_url(), '/data/land-plot-detail/1')

    def test_verbose_names(self):
        self.assertEquals(LandPlot._meta.verbose_name, 'участок')
        self.assertEquals(LandPlot._meta.verbose_name_plural, 'участки')
