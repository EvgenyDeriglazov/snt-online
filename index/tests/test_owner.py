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
from django.contrib.auth.models import User
from index.models import *
import datetime

class OwnerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(
            username="user1",
            password="mypass",
        )
        Owner.objects.create(
            first_name="Сергей",
            middle_name="Сергеевич",
            last_name="Сергеев",
            phone="+79990001122",
            email="my@email.com",
            user=User.objects.get(id=1),
            join_date=datetime.date.today(),
        )

   # Model fields properties tests
    def test_first_name_field(self):
        obj = Owner.objects.get(id=1)
        field = obj._meta.get_field('first_name')
        self.assertEquals(field.verbose_name, "Имя")
        self.assertEquals(field.max_length, 50)
        self.assertEquals(field.help_text, "Введите имя")
        self.assertEquals(field.validators[0:1], [validate_human_names])
        self.assertEquals(obj.first_name, "Сергей")
       
    def test_middle_name_field(self):
        obj = Owner.objects.get(id=1)
        field = obj._meta.get_field('middle_name')
        self.assertEquals(field.verbose_name, "Отчество")
        self.assertEquals(field.max_length, 50)
        self.assertEquals(field.help_text, "Введите отчество")
        self.assertEquals(field.validators[0:1], [validate_human_names])
        self.assertEquals(obj.middle_name, "Сергеевич")
    
    def test_last_name_field(self):
        obj = Owner.objects.get(id=1)
        field = obj._meta.get_field('last_name')
        self.assertEquals(field.verbose_name, "Фамилия")
        self.assertEquals(field.max_length, 50)
        self.assertEquals(field.help_text, "Введите фамилию")
        self.assertEquals(field.validators[0:1], [validate_human_names])
        self.assertEquals(obj.last_name, "Сергеев")

    def test_phone_field(self):
        obj = Owner.objects.get(id=1)
        field = obj._meta.get_field('phone')
        self.assertEquals(field.verbose_name, "Номер телефона")
        self.assertEquals(field.max_length, 12)
        self.assertEquals(field.help_text, "Укажите номер в формате +7xxxxxxxxxx")
        self.assertEquals(field.validators[0:1], [validate_phone])
        self.assertEquals(field.unique, True)
        self.assertEquals(field.blank, True)
        self.assertEquals(field.null, True)
        self.assertEquals(obj.phone, "+79990001122")

    def test_email_field(self):
        obj = Owner.objects.get(id=1)
        field = obj._meta.get_field('email')
        self.assertEquals(field.verbose_name, "Почта")
        self.assertEquals(field.help_text, "Адрес электронной почты")
        self.assertEquals(field.unique, True)
        self.assertEquals(field.blank, True)
        self.assertEquals(field.null, True)
        self.assertEquals(obj.email, "my@email.com")
   
    def test_user_field(self):
        obj = Owner.objects.get(id=1)
        user_obj = User.objects.get(id=1)
        field = obj._meta.get_field('user')
        self.assertEquals(field.verbose_name, "Логин")
        self.assertEquals(field.help_text, "Аккаунт пользователя на сайте")
        self.assertEquals(
            field.validators[0:2],
            [validate_accountant_user, validate_chair_man_user]
            )
        self.assertEquals(field.blank, True)
        self.assertEquals(field.null, True)
        self.assertEquals(obj.user, user_obj)
    
    def test_join_date_field(self):
        obj = Owner.objects.get(id=1)
        field = obj._meta.get_field('join_date')
        self.assertEquals(field.verbose_name, "Дата вступления в СНТ")
        self.assertEquals(field.help_text, "Укажите дату вступления в члены СНТ")
        self.assertEquals(obj.join_date, datetime.date.today())

    def test_leave_date_field(self):
        obj = Owner.objects.get(id=1)
        field = obj._meta.get_field('leave_date')
        self.assertEquals(field.verbose_name, "Дата выхода из СНТ")
        self.assertEquals(field.help_text, "Укажите дату выхода из членов СНТ")
        self.assertEquals(field.blank, True)
        self.assertEquals(field.null, True)
        self.assertEquals(obj.leave_date, None)

    def test_meta_options(self):
        self.assertEquals(Owner._meta.verbose_name, "владелец")
        self.assertEquals(Owner._meta.verbose_name_plural, "владельцы")
        self.assertEquals(len(Owner._meta.constraints), 4)
        self.assertEquals(Owner._meta.constraints[0].fields, ('email',))
        self.assertEquals(
            Owner._meta.constraints[0].name,
            'index_owner_email_unique_constraint'
            )
        self.assertEquals(Owner._meta.constraints[1].fields, ('phone',))
        self.assertEquals(
            Owner._meta.constraints[1].name,
            'index_owner_phone_unique_constraint'
            )
        self.assertEquals(Owner._meta.constraints[2].fields, ('join_date',))
        self.assertEquals(
            Owner._meta.constraints[2].name,
            'index_owner_join_date_unique_constraint'
            )
        self.assertEquals(Owner._meta.constraints[3].fields, ('leave_date',))
        self.assertEquals(
            Owner._meta.constraints[3].name,
            'index_owner_leave_date_unique_constraint'
            )

    def test_str_method(self):
        obj = Owner.objects.get(id=1)
        obj_name = f"{obj.last_name} {obj.first_name} {obj.middle_name}"
        self.assertEquals(obj_name, obj.__str__())
        # or self.assertEquals(object_name, str(lp_obj))
    
    def test_get_absolute_url(self):
        obj = Owner.objects.get(id=1)
        self.assertEquals(obj.get_absolute_url(), None)

    def test_http404_accountant_exists_in_save_method(self):
         """Test Http404 when user taken by accountant"""
         Owner.objects.all().delete()
         Accountant.objects.create(
             first_name='Иван',
             middle_name='Иванович',
             last_name='Иванов',
             user=User.objects.get(id=1),
             join_date=datetime.date.today()
             )
         with self.assertRaises(Http404):
             Owner.objects.create(
                 first_name='Иван',
                 middle_name='Иванович',
                 last_name='Иванов',
                 user=User.objects.get(id=1),
                 join_date=datetime.date.today()
                 )

    def test_http404_chair_man_exists_in_save_method(self):
         """Test Http404 when user taken by chair man"""
         Owner.objects.all().delete()
         ChairMan.objects.create(
             first_name='Иван',
             middle_name='Иванович',
             last_name='Иванов',
             user=User.objects.get(id=1),
             join_date=datetime.date.today()
             )
         with self.assertRaises(Http404):
             Owner.objects.create(
                 first_name='Иван',
                 middle_name='Иванович',
                 last_name='Иванов',
                 user=User.objects.get(id=1),
                 join_date=datetime.date.today()
                 )

    def test_owner_user_exists(self):
        """Test for helper function owner_user_exists()."""
        obj = User.objects.get(id=1)
        self.assertEqual(owner_user_exists(obj), True)
        obj2 = User.objects.create(
            username="username",
            password="password",
            )
        self.assertEqual(owner_user_exists(obj2), None)
