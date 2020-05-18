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
from datetime import datetime
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
            title='Мой заголовок',
            body='Мой текст',
            author=ChairMan.objects.get(id=1),
            )
        
    # Test functions
    def test_pub_date_field(self):
        obj = Info.objects.get(id=1)
        field_label = obj._meta.get_field('pub_date').verbose_name
        auto_now_add = obj._meta.get_field('pub_date').auto_now_add
        help_text = obj._meta.get_field('pub_date').help_text 
        blank = obj._meta.get_field('pub_date').blank 
        self.assertEqual(field_label, "Дата публикации")
        self.assertEqual(auto_now_add, True)
        self.assertEqual(help_text, "Дата и время публикации")
        self.assertEqual(blank, True)
        self.assertEqual(type(obj.pub_date), type(datetime.now()))

    def test_title_field(self):
        obj = Info.objects.get(id=1)
        field_label = obj._meta.get_field('title').verbose_name
        max_length = obj._meta.get_field('title').max_length
        help_text = obj._meta.get_field('title').help_text 
        self.assertEqual(field_label, "Заголовок")
        self.assertEqual(max_length, 200)
        self.assertEqual(help_text, "Заголовок объявления")
        self.assertEqual(obj.title, "Мой заголовок")

    def test_body_field(self):
        obj = Info.objects.get(id=1)
        field_label = obj._meta.get_field('body').verbose_name
        help_text = obj._meta.get_field('body').help_text 
        self.assertEqual(field_label, "Текст")
        self.assertEqual(help_text, "Текст объявления")
        self.assertEqual(obj.body, "Мой текст")

    def test_author_field(self):
        obj = Info.objects.get(id=1)
        author_obj = ChairMan.objects.get(id=1)
        field_label = obj._meta.get_field('author').verbose_name
        help_text = obj._meta.get_field('author').help_text
        #on_delete = obj._meta.get_field('author').on_delete
        self.assertEqual(field_label, "Автор")
        self.assertEqual(help_text, "Автор объявления (действующий председатель)")
        #self.assertEqual(obj_field.on_delete, models.SET_NULL)
        self.assertEqual(obj.author, author_obj)

    def test_object_name(self):
        obj = Info.objects.get(id=1)
        object_name = f'{obj}'
        self.assertEquals(object_name, obj.__str__())
        # or self.assertEquals(object_name, str(obj))
    
    def test_get_absolute_url(self):
        obj = Info.objects.get(id=1)
        self.assertEquals(obj.get_absolute_url(), '/data/land-plot-detail/1')

    def test_verbose_names(self):
        self.assertEquals(LandPlot._meta.verbose_name, 'участок')
        self.assertEquals(LandPlot._meta.verbose_name_plural, 'участки')
