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
# from django.contrib.auth.models import User

class InfoModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        ChairMan.objects.create(
            first_name='Иван',
            middle_name='Иванович',
            last_name='Иванов',
            )
        Info.objects.create(
            title='Заголовок',
            body='Текст',
            author=ChairMan.objects.get(id=1),
            )
        
    # Test functions
    def test_title_field(self):
        obj = Info.objects.get(id=1)
        field_label = obj._meta.get_field('title').verbose_name
        max_length = obj._meta.get_field('title').max_length
        help_text = obj._meta.get_field('title').help_text 
        unique_prop = obj._meta.get_field('plot_number').unique
        self.assertEqual(field_label, "Номер участка")
        self.assertEqual(max_length, 10)
        self.assertEqual(help_text, "Номер участка")
        self.assertEqual(unique_prop, True)
        self.assertEqual(obj.plot_number, "10")

    def test_plot_area_field(self):
        obj = LandPlot.objects.get(id=1)
        field_label = obj._meta.get_field('plot_area').verbose_name
        help_text = obj._meta.get_field('plot_area').help_text 
        self.assertEqual(field_label, "Размер участка")
        self.assertEqual(help_text, "Единица измерения кв.м")
        self.assertEqual(obj.plot_area, 6000)

    def test_snt_field(self):
        obj = LandPlot.objects.get(id=1)
        snt_obj = Snt.objects.get(id=1)
        field_label = obj._meta.get_field('snt').verbose_name
        help_text = obj._meta.get_field('snt').help_text 
        self.assertEqual(field_label, "СНТ")
        self.assertEqual(help_text, "Расположен в СНТ")
        self.assertEqual(obj.snt, snt_obj)

    def test_owner_field(self):
        obj = LandPlot.objects.get(id=1)
        owner_obj = Owner.objects.get(id=1)
        field_label = obj._meta.get_field('owner').verbose_name
        help_text = obj._meta.get_field('owner').help_text
        is_null = obj._meta.get_field('owner').null
        #on_delete = obj._meta.get_field('owner').on_delete
        self.assertEqual(field_label, "владелец участка")
        self.assertEqual(help_text, "Владелец участка")
        self.assertEqual(is_null, True)
        #self.assertEqual(on_delete, models.SET_NULL)
        self.assertEqual(obj.owner, owner_obj)

    def test_object_name(self):
        obj = LandPlot.objects.get(id=1)
        object_name = f'{obj.plot_number}'
        self.assertEquals(object_name, obj.__str__())
        # or self.assertEquals(object_name, str(obj))
    
    def test_get_absolute_url(self):
        obj = LandPlot.objects.get(id=1)
        self.assertEquals(obj.get_absolute_url(), '/data/land-plot-detail/1')

    def test_verbose_names(self):
        self.assertEquals(LandPlot._meta.verbose_name, 'участок')
        self.assertEquals(LandPlot._meta.verbose_name_plural, 'участки')
