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
from django.http import Http404
import datetime

class AccountantModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(
            username="username",
            password="password",
            )
        Accountant.objects.create(
            first_name='Иван',
            middle_name='Иванович',
            last_name='Иванов',
            user=User.objects.get(id=1),
            join_date=datetime.date.today()
            )
    # Test functions
    def test_first_name_field(self):
        obj = Accountant.objects.get(id=1)
        field = obj._meta.get_field('first_name')
        self.assertEquals(field.verbose_name, "Имя")
        self.assertEquals(field.max_length, 50)
        self.assertEquals(field.validators[0:1], [validate_human_names])
        self.assertEquals(field.help_text, "Введите имя")

    def test_middle_name_field(self):
        obj = Accountant.objects.get(id=1)
        field = obj._meta.get_field('middle_name')
        self.assertEquals(field.verbose_name, "Отчество")
        self.assertEquals(field.max_length, 50)
        self.assertEquals(field.validators[0:1], [validate_human_names])
        self.assertEquals(field.help_text, "Введите отчество")
    
    def test_last_name_field(self):
        obj = Accountant.objects.get(id=1)
        field = obj._meta.get_field('last_name')
        self.assertEquals(field.verbose_name, "Фамилия")
        self.assertEquals(field.max_length, 50)
        self.assertEquals(field.validators[0:1], [validate_human_names])
        self.assertEquals(field.help_text, "Введите фамилию")

    def test_phone_field(self):
        obj = Accountant.objects.get(id=1)
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
        obj = Accountant.objects.get(id=1)
        field = obj._meta.get_field('email')
        self.assertEquals(field.verbose_name, "Почта")
        self.assertEquals(field.unique, True)
        self.assertEquals(field.blank, True)
        self.assertEquals(field.null, True)
        self.assertEquals(field.help_text, "Адрес электронной почты")
    
    def test_user_field(self):
        obj = Accountant.objects.get(id=1)
        user_obj = User.objects.get(id=1)
        field = obj._meta.get_field('user')
        self.assertEquals(field.verbose_name, "Логин")
        self.assertEquals(field.help_text, "Аккаунт пользователя на сайте")
        self.assertEquals(field.blank, True)
        self.assertEquals(field.null, True)
        self.assertEquals(obj.user, user_obj)
        self.assertEquals(
            field.validators[0:2],
            [validate_owner_user, validate_chair_man_user]
            )
   
    def test_join_date_field(self):
        obj = Accountant.objects.get(id=1)
        field = obj._meta.get_field('join_date')
        self.assertEquals(field.verbose_name, "Дата вступления в должность")
        self.assertEquals(field.help_text, "Укажите дату вступления в должность")
        self.assertEquals(obj.join_date, datetime.date.today())

    def test_leave_date_field(self):
        obj = Accountant.objects.get(id=1)
        field = obj._meta.get_field('leave_date')
        self.assertEquals(field.verbose_name, "Дата ухода с должности")
        self.assertEquals(field.help_text, "Укажите дату ухода с должности")
        self.assertEquals(field.blank, True)
        self.assertEquals(field.null, True)
        self.assertEquals(obj.leave_date, None) 

    def test_meta_options(self):
        self.assertEquals(Accountant._meta.verbose_name, "бухгалтер")
        self.assertEquals(Accountant._meta.verbose_name_plural, "бухгалтеры")
        self.assertEquals(len(Accountant._meta.constraints), 4)
        self.assertEquals(
            Accountant._meta.constraints[0].fields,
            ('email',)
            )
        self.assertEquals(
            Accountant._meta.constraints[0].name,
            'index_accountant_email_unique_constraint'
            )
        self.assertEquals(
            Accountant._meta.constraints[1].fields,
            ('phone',)
            )
        self.assertEquals(
            Accountant._meta.constraints[1].name,
            'index_accountant_phone_unique_constraint'
            )
        self.assertEquals(
            Accountant._meta.constraints[2].fields,
            ('join_date',)
            )
        self.assertEquals(
            Accountant._meta.constraints[2].name,
            'index_accountant_join_date_unique_constraint'
            )
        self.assertEquals(
            Accountant._meta.constraints[3].fields,
            ('leave_date',)
            )
        self.assertEquals(
            Accountant._meta.constraints[3].name,
            'index_accountant_leave_date_unique_constraint'
            )

    def test_str_method(self):
        obj = Accountant.objects.get(id=1)
        object_name = f"{obj.last_name} {obj.first_name} {obj.middle_name}"
        self.assertEquals(object_name, obj.__str__())

    def test_get_absolute_url(self):
        obj = Accountant.objects.get(id=1)
        self.assertEquals(obj.get_absolute_url(), None)

    def test_midification_in_save_method(self):
       # Check possibility of current accountant modification
        Accountant.objects.filter(id=1).update(
            join_date=datetime.date.today() - datetime.timedelta(days=1),
            leave_date=datetime.date.today(),
            )
        accountant = Accountant.objects.get(id=1)
        self.assertEqual(
            accountant.join_date,
            datetime.date.today() - datetime.timedelta(days=1),
            )
        self.assertEqual(accountant.leave_date, datetime.date.today())

    def test_create_2_accountants_in_save_method(self):
        """Test possibility of creating 2nd accountant without error."""
        Accountant.objects.filter(id=1).update(
            join_date=datetime.date.today() - datetime.timedelta(days=1),
            leave_date=datetime.date.today(),
            )
        User.objects.create(
            username="username1",
            password="password1",
            )
        Accountant.objects.create(
            first_name='Иван',
            middle_name='Иванович',
            last_name='Иванов',
            user=User.objects.get(id=2),
            join_date=datetime.date.today()
            )
        self.assertEqual(len(Accountant.objects.all()), 2)

    def test_create_first_accountant_in_save_method(self):
        """Test creating first accoutnant."""
        Accountant.objects.all().delete()
        self.assertEqual(len(Accountant.objects.all()), 0)
        Accountant.objects.create(
            first_name='Иван',
            middle_name='Иванович',
            last_name='Иванов',
            user=User.objects.get(id=1),
            join_date=datetime.date.today()
            )
        self.assertEqual(len(Accountant.objects.all()), 1)

    def test_http404_2_accountants_in_save_method(self):
        """Test for creating 2nd accountant with error."""
        User.objects.create(
            username="username1",
            password="password1",
            )
        with self.assertRaises(Http404):
            Accountant.objects.create(
                first_name='Иван',
                middle_name='Иванович',
                last_name='Иванов',
                user=User.objects.get(id=2),
                join_date=datetime.date.today()
                )

    def test_http404_owner_exists_in_save_method(self):
        """Test Http404 when user taken by owner"""
        Accountant.objects.all().delete()
        Owner.objects.create(
            first_name='Иван',
            middle_name='Иванович',
            last_name='Иванов',
            user=User.objects.get(id=1),
            join_date=datetime.date.today()
            )
        with self.assertRaises(Http404):
            Accountant.objects.create(
                first_name='Иван',
                middle_name='Иванович',
                last_name='Иванов',
                user=User.objects.get(id=1),
                join_date=datetime.date.today()
                )   

    def test_http404_chair_man_exists_in_save_method(self):
        """Test Http404 when user taken by chair man"""
        Accountant.objects.all().delete()
        ChairMan.objects.create(
            first_name='Иван',
            middle_name='Иванович',
            last_name='Иванов',
            user=User.objects.get(id=1),
            join_date=datetime.date.today()
            )
        with self.assertRaises(Http404):
            Accountant.objects.create(
                first_name='Иван',
                middle_name='Иванович',
                last_name='Иванов',
                user=User.objects.get(id=1),
                join_date=datetime.date.today()
                )   

    def test_accountant_user_exists(self):
        """Test for helper function accountant_user_exists()."""
        obj = User.objects.get(id=1)
        self.assertEqual(accountant_user_exists(obj), True)
        obj2 = User.objects.create(
            username="username1",
            password="password2",
            )
        self.assertEqual(accountant_user_exists(obj2), None)
