# --- Collectstatic (ValueError: Missing staticfiles manifest entry...) ---
#  $python3 manage.py collectstatic
# --- Verbosity ---
#  $python3 manage.py test --verbosity (1-default, 0, 1, 2, 3)
# --- Run specific test modules ---
#  $python3 manage.py test data.tests
#  $python3 manage.py test data.tests.test_models
#  $python3 manage.py test data.tests.test_models.TestClass
# --- Coverage.py --- 
#  $coverage run --source='.' manage.py test <appname>
#  $coverage report
# --- FIXTURES ---
# use command below
# python3 manage.py dumpdata -e contenttypes -e auth.Permission  > all_db.json
# then move the json file to appname.fixtures directory

import unittest
from django.test import TestCase
from index.models import *
import datetime

class TestHomePage(TestCase):
    # Test functions
    def test_home_page_response(self):
        """"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_home_page_template(self):
        """"""
        response = self.client.get('')
        self.assertTemplateUsed(response, 'home_page.html')

class TestInfoPage(TestCase):
    # Test functions
    def test_info_page_response(self):
        """"""
        response = self.client.get('/info/')
        self.assertEqual(response.status_code, 200)

    def test_info_page_template(self):
        """"""
        response = self.client.get('/info/')
        self.assertTemplateUsed(response, 'info_page.html')

class TestInfoDetailsPage(TestCase):
    fixtures = ['all_db.json']

    # Test functions
    def test_info_details_page_response(self):
        """"""
        response = self.client.get('/info/1')
        self.assertEqual(response.status_code, 200)

    def test_info_details_page_template(self):
        """"""
        response = self.client.get('/info/1')
        self.assertTemplateUsed(response, 'info_details_page.html')

class TestBankDetailsPage(TestCase):
    """"""
    #fixtures = ['all_db.json']

    # Test functions
    def test_bank_details_page_response(self):
        """"""
        response = self.client.get('/snt-bank-details/')
        self.assertEqual(response.status_code, 200)

    def test_bank_details_page_template(self):
        """"""
        response = self.client.get('/snt-bank-details/')
        self.assertTemplateUsed(response, 'snt_bank_details_page.html')

class TestSntContactsPage(TestCase):
    """"""
    fixtures = ['all_db.json']

    # Test functions
    def test_snt_contacts_page_response(self):
        """"""
        response = self.client.get('/contacts/')
        self.assertEqual(response.status_code, 200)

    def test_snt_contacts_page_template(self):
        """"""
        response = self.client.get('/contacts/')
        self.assertTemplateUsed(response, 'snt_contacts_page.html')

class TestDocsPage(TestCase):
    """"""
    #fixtures = ['all_db.json']

    # Test functions
    def test_docs_page_response(self):
        """"""
        response = self.client.get('/docs/')
        self.assertEqual(response.status_code, 200)

    def test_docs_page_template(self):
        """"""
        response = self.client.get('/docs/')
        self.assertTemplateUsed(response, 'docs_page.html')

class TestDocsDetailsPage(TestCase):
    """"""
    fixtures = ['all_db.json']

    # Test functions
    def test_docs_page_response(self):
        """"""
        response = self.client.get('/docs/1')
        self.assertEqual(response.status_code, 200)

    def test_docs_page_template(self):
        """"""
        response = self.client.get('/docs/1')
        self.assertTemplateUsed(response, 'docs_details_page.html')

