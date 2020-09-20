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
# use commands below
# python3 manage.py dumpdata -e contenttypes -e auth.Permission  > test_db.json
# python3 manage.py dumpdata --indent 4 --exclude contenttypes --format json >
# test_db.json
# then move the json file to appname.fixtures directory

from django.test import TestCase, Client, tag
from index.models import *
from django.contrib.auth.forms import AuthenticationForm

@tag('views', 'index', 'index-views')
class TestHomePage(TestCase):
    """"""
    fixtures = ['test_db.json']
    # Test functions
    def test_home_page_url(self):
        """"""
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_home_page_url_conf_name(self):
        """"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_page_template(self):
        """"""
        response = self.client.get('')
        self.assertTemplateUsed(response, 'home_page.html')

    def test_home_page_context_keys_for_unauth_user(self):
        """Test context dict keys for unauthenticated user."""
        response = self.client.get('')
        self.assertIn('snt_list', response.context)
        self.assertIn('land_plots_count', response.context)
        self.assertIn('auth_form', response.context)
        self.assertIn('user_name', response.context)
        self.assertIn('land_plots', response.context)

    def test_home_page_context_values_for_unauth_user(self):
        """Test context dict values."""
        response = self.client.get('')
        self.assertEqual(len(response.context['snt_list']), 1)
        self.assertEqual(response.context['land_plots_count'], 4)
        self.assertNotIsInstance(
            response.context['auth_form'],
            AuthenticationForm,
            )
        self.assertEqual(response.context['user_name'], 'None')
        self.assertEqual(response.context['land_plots'], None)

    def test_home_page_redirectsfor_auth_user(self):
        """Test redirects for authenticated user to land plot page."""
        self.client.login(username='owner1', password='pswd5000')
        response = self.client.get('')
        self.assertRedirects(response, '/plot-id-1/')

 
