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
import datetime

class ChairManModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(
            username="username",
            password="password",
            )
        ChairMan.objects.create(
            first_name='Иван',
            middle_name='Иванович',
            last_name='Иванов',
            user=User.objects.get(id=1),
            join_date=datetime.date.today(),
            )
    # Test functions
    def test_first_name_field(self):
        obj = ChairMan.objects.get(id=1)
        field = obj._meta.get_field('first_name')
        self.assertEquals(field.verbose_name, "Имя")
        self.assertEquals(field.max_length, 50)
        self.assertEquals(field.validators[0:1], [validate_human_names])
        self.assertEquals(field.help_text, "Введите имя")

    def test_middle_name_field(self):
        obj = ChairMan.objects.get(id=1)
        field = obj._meta.get_field('middle_name')
        self.assertEquals(field.verbose_name, "Отчество")
        self.assertEquals(field.max_length, 50)
        self.assertEquals(field.validators[0:1], [validate_human_names])
        self.assertEquals(field.help_text, "Введите отчество")
    
    def test_last_name_field(self):
        obj = ChairMan.objects.get(id=1)
        field = obj._meta.get_field('last_name')
        self.assertEquals(field.verbose_name, "Фамилия")
        self.assertEquals(field.max_length, 50)
        self.assertEquals(field.validators[0:1], [validate_human_names])
        self.assertEquals(field.help_text, "Введите фамилию")

    def test_phone_field(self):
        obj = ChairMan.objects.get(id=1)
        field = obj._meta.get_field('phone')
        self.assertEquals(field.verbose_name, "Номер телефона")
        self.assertEquals(field.max_length, 12)
        self.assertEquals(
            field.help_text,
            "Укажите номер в формате +7xxxxxxxxxx"
            )
        self.assertEquals(field.unique, True)
        self.assertEquals(field.blank, True)
        self.assertEquals(field.null, True)
        self.assertEquals(field.validators[0:1], [validate_phone])

    def test_email_field(self):
        obj = ChairMan.objects.get(id=1)
        field = obj._meta.get_field('email')
        self.assertEquals(field.verbose_name, "Почта")
        self.assertEquals(field.unique, True)
        self.assertEquals(field.blank, True)
        self.assertEquals(field.null, True)
        self.assertEquals(field.help_text, "Адрес электронной почты")
    
    def test_user_field(self):
        obj = ChairMan.objects.get(id=1)
        user_obj = User.objects.get(id=1)
        field = obj._meta.get_field('user')
        self.assertEquals(field.verbose_name, "Логин")
        self.assertEquals(field.help_text, "Аккаунт пользователя на сайте")
        self.assertEquals(field.blank, True)
        self.assertEquals(field.null, True)
        self.assertEquals(obj.user, user_obj)
        self.assertEquals(field.validators[0:1], [validate_chair_man_user])
 
    def test_join_date_field(self):
        obj = ChairMan.objects.get(id=1)
        field = obj._meta.get_field('join_date')
        self.assertEquals(field.verbose_name, "Дата вступления в должность")
        self.assertEquals(field.help_text, "Укажите дату вступления в должность")
        self.assertEquals(obj.join_date, datetime.date.today())

    def test_leave_date_field(self):
        obj = ChairMan.objects.get(id=1)
        field = obj._meta.get_field('leave_date')
        self.assertEquals(field.verbose_name, "Дата ухода с должности")
        self.assertEquals(field.help_text, "Укажите дату ухода с должности")
        self.assertEquals(field.blank, True)
        self.assertEquals(field.null, True)
        self.assertEquals(obj.leave_date, None)

    def test_meta_options(self):
        self.assertEquals(ChairMan._meta.verbose_name, "председатель")
        self.assertEquals(ChairMan._meta.verbose_name_plural, "председатели")
        self.assertEquals(len(ChairMan._meta.constraints), 4)
        self.assertEquals(
            ChairMan._meta.constraints[0].fields,
            ('join_date',)
            )
        self.assertEquals(
            ChairMan._meta.constraints[0].name,
            'index_chairman_join_date_unique_constraint'
            )
        self.assertEquals(
            ChairMan._meta.constraints[1].fields,
            ('leave_date',)
            )
        self.assertEquals(
            ChairMan._meta.constraints[1].name,
            'index_chairman_leave_date_unique_constraint'
            )
        self.assertEquals(
            ChairMan._meta.constraints[2].fields,
            ('email',)
            )
        self.assertEquals(
            ChairMan._meta.constraints[2].name,
            'index_chairman_email_unique_constraint'
            )
        self.assertEquals(
            ChairMan._meta.constraints[3].fields,
            ('phone',)
            )
        self.assertEquals(
            ChairMan._meta.constraints[3].name,
            'index_chairman_phone_unique_constraint'
            )
 

    def test_str_method(self):
        obj = ChairMan.objects.get(id=1)
        object_name = f"{obj.last_name} {obj.first_name} {obj.middle_name}"
        self.assertEquals(object_name, obj.__str__())

    def test_get_absolute_url(self):
        obj = ChairMan.objects.get(id=1)
        self.assertEquals(obj.get_absolute_url(), None)


