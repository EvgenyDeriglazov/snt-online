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
import datetime
# from django.contrib.auth.models import User

class InfoModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        ChairMan.objects.create(
            first_name='Иван',
            middle_name='Иванович',
            last_name='Иванов',
            join_date=datetime.date.today(),
            )
        Info.objects.create(
            title='Мой заголовок',
            body='Мой текст',
            author=ChairMan.objects.get(id=1),
            )
        
    # Test functions
    def test_pub_date_field(self):
        # Attributes test
        field = Info._meta.get_field('pub_date')
        self.assertEqual(field.verbose_name, "Дата публикации")
        self.assertEqual(field.auto_now_add, True)
        self.assertEqual(field.help_text, "Дата и время публикации")
        self.assertEqual(field.blank, True)
        # Data test
        obj = Info.objects.get(id=1)
        self.assertEqual(type(obj.pub_date), type(datetime.datetime.now()))

    def test_title_field(self):
        # Attributes test
        field = Info._meta.get_field('title')
        self.assertEqual(field.verbose_name, "Заголовок")
        self.assertEqual(field.max_length, 200)
        self.assertEqual(field.help_text, "Заголовок объявления")
        # Data test
        obj = Info.objects.get(id=1)
        self.assertEqual(obj.title, "Мой заголовок")

    def test_body_field(self):
        # Attributes test
        field = Info._meta.get_field('body')
        self.assertEqual(field.verbose_name, "Текст")
        self.assertEqual(field.help_text, "Текст объявления")
        # Data test
        obj = Info.objects.get(id=1)
        self.assertEqual(obj.body, "Мой текст")

    def test_author_field(self):
        # Attributes test
        field = Info._meta.get_field('author')
        #on_delete = obj._meta.get_field('author').on_delete
        self.assertEqual(field.verbose_name, "Автор")
        self.assertEqual(field.help_text, "Автор объявления (действующий председатель)")
        #self.assertEqual(obj_field.on_delete, models.SET_NULL)
        # Data test
        obj = Info.objects.get(id=1)
        author_obj = ChairMan.objects.get(id=1)
        self.assertEqual(obj.author, author_obj)

    def test_status_field(self):
        # Attributes test
        field = Info._meta.get_field('status')
        STATUS_CHOICES = [
            ('published', 'Опубликовано'),
            ('unpublished', 'Неопубликовано'),
            ]
        self.assertEqual(field.verbose_name, "Статус")
        self.assertEqual(field.max_length, 11)
        self.assertEqual(
            field.help_text,
            "Выберите статус для публикации или снятия с публикации"
            )
        self.assertEqual(field.choices, STATUS_CHOICES)
        self.assertEqual(field.default, 'unpublished')
        # Data test
        obj = Info.objects.get(id=1)
        self.assertEqual(obj.status, 'unpublished')


    def test_meta_options(self):
        self.assertEquals(Info._meta.verbose_name, "информация")
        self.assertEquals(Info._meta.verbose_name_plural, "информация")

    def test_str_method(self):
        obj = Info.objects.get(id=1)
        object_name = f"{obj.title}"
        self.assertEquals(object_name, obj.__str__())
        # or self.assertEquals(object_name, str(obj))
    
    def test_get_absolute_url(self):
        obj = Info.objects.get(id=1)
        self.assertEquals(obj.get_absolute_url(), None)
