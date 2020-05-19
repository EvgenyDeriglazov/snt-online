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
from datetime import date
from decimal import *
from django.utils.translation import gettext_lazy as _

class DateValidatorsTest(TestCase):
    # Set up non-modified objects used by all test methods
    correct_phone = "+79998887766"
    wrong_phone = "+7999888776g"

    def test_wrong_number(self):
        self.assertRaises(ValidationError, validate_number, '124gf')
        self.assertRaisesRegex(
            ValidationError,
            "['Некорректный символ - (g, f)']",
            validate_number,
            '124gf',
        )
        # Same as previous (example)
        with self.assertRaisesRegex(
            ValidationError,
            "['Некорректный символ - (g, f)']",
        ):validate_number('124gf')

    def test_validate_20_length(self):
        value = ""
        for i in range(19):
            value += "1"
            self.assertRaises(ValidationError, validate_20_length, value)
            self.assertRaisesRegex(
                ValidationError,
                "['Неверный номер (меньше 20-и знаков)']",
                validate_20_length,
                value,
            )
        value += "1"
        validate_20_length(value)
    
    def test_validate_10_length(self):
        value = ""
        for i in range(9):
            value += "1"
            self.assertRaises(ValidationError, validate_10_length, value)
            self.assertRaisesRegex(
                ValidationError,
                "['Неверный номер (меньше 10-и знаков)']",
                validate_10_length,
                value,
            )
        value += "1"
        validate_10_length(value)
 
    def test_validate_9_length(self):
        value = ""
        for i in range(8):
            value += "1"
            self.assertRaises(ValidationError, validate_9_length, value)
            self.assertRaisesRegex(
                ValidationError,
                "['Неверный номер (меньше 9-и знаков)']",
                validate_9_length,
                value,
            )
        value += "1"
        validate_9_length(value)
 
    def test_validate_human_names(self):
        value = ""
        for i in range(1040):
            value = chr(i)
            self.assertRaises(ValidationError, validate_human_names, value)
            self.assertRaisesRegex(
                ValidationError,
                "['Можно использовать только русские символы']",
                validate_human_names,
                value,
            )
        value = ""
        for i in range(1104, 1279):
            value = chr(i)
            self.assertRaises(ValidationError, validate_human_names, value)
            self.assertRaisesRegex(
                ValidationError,
                "['Можно использовать только русские символы']",
                validate_human_names,
                value,
            )

    def test_validate_phone(self):
        value = ""
        for i in range(57, 49):
            if i == 43:
                continue
            value = chr(i)
        self.assertRaises(ValidationError, validate_phone, "+7999888776g")
        self.assertRaisesRegex(
            ValidationError,
            #"['Некорректный символ - (r)']",
            "[Некорректный]",
            validate_phone,
            "+7999888776r",
            )
        self.assertRaisesRegex(
            ValidationError,
            "['Неверный формат номера - 079998887766']",
            validate_phone,
            "079998887766",
            )

 
