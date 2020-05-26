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
from django.contrib.auth.models import User

class DocsModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(
            username="username",
            password="password",
            )
        Docs.objects.create(
            #upload_to={'name': "test_file.x"},
            title="Тестовый документ",
            doc_user=User.objects.get(id=1),
            )
      
    # Test functions
    def test_upload_date_field(self):
        # Attributes test
        field = Docs._meta.get_field('upload_date')
        self.assertEqual(field.verbose_name, "Дата загрузки")
        self.assertEqual(field.auto_now_add, True)
        self.assertEqual(field.help_text, "Дата загрузки документа")
        self.assertEqual(field.blank, True)
        # Data test
        obj = Docs.objects.get(id=1)
        self.assertEqual(obj.upload_date, datetime.date.today())

    def test_title_field(self):
        # Attributes test
        field = Docs._meta.get_field('title')
        self.assertEqual(field.verbose_name, "Название документа")
        self.assertEqual(field.max_length, 200)
        self.assertEqual(field.help_text, "Укажите название документа")
        # Data test
        obj = Docs.objects.get(id=1)
        self.assertEqual(obj.title, "Тестовый документ")

    def test_upload_field(self):
        # Attributes test
        field = Docs._meta.get_field('upload')
        self.assertEqual(field.verbose_name, "Файл документа")
        self.assertEqual(field.help_text, "Выберите файл для загрузки")
        # Data test
        obj = Docs.objects.get(id=1)
        self.assertEqual(obj.upload.name, '')

    def test_doc_user_field(self):
        # Attributes test
        field = Docs._meta.get_field('doc_user')
        #on_delete = obj._meta.get_field('author').on_delete
        self.assertEqual(field.verbose_name, "Пользователь")
        #self.assertEqual(obj_field.on_delete, models.SET_NULL)
        # Data test
        obj = Docs.objects.get(id=1)
        doc_user_obj = User.objects.get(id=1)
        self.assertEqual(obj.doc_user, doc_user_obj)

    def test_status_field(self):
         # Attributes test
         field = Docs._meta.get_field('status')
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
         obj = Docs.objects.get(id=1)
         self.assertEqual(obj.status, 'unpublished')


    def test_meta_options(self):
        self.assertEquals(Docs._meta.verbose_name, "документ")
        self.assertEquals(Docs._meta.verbose_name_plural, "документы")

    def test_str_method(self):
        obj = Docs.objects.get(id=1)
        object_name = f"{obj.title}"
        self.assertEquals(object_name, obj.__str__())
        # or self.assertEquals(object_name, str(obj))
    
    def test_get_absolute_url(self):
        obj = Docs.objects.get(id=1)
        self.assertEquals(obj.get_absolute_url(), "/data/land-plot-detail/1")
