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
# use commands below (choose one of 2) to create fixture from db
# python3 manage.py dumpdata -e contenttypes -e auth.Permission  > test_db.json
# python3 manage.py dumpdata --indent 4 --exclude contenttypes --format json >
# test_db.json
# then move the json file to appname.fixtures directory

from django.test import TestCase, Client, tag
from index.models import *
from membership.models import *
from django.contrib.auth.forms import AuthenticationForm
#from membership.forms import *
import datetime
import json

# response is a TemplateResponse object

@tag('views', 'membership', 'membership-views')
class MembershipPaymentsPage(TestCase):
    """MembershipPaymentsPage in Membership app view."""
    fixtures = ['test_db.json']

    # Test URL access
    def test_membership_page_url_by_unauthenticated_user(self):
        """"""
        response = self.client.get('/plot-id-1/membership/')
        self.assertEqual(response.status_code, 302)

    def test_membership_page_url_by_super_user(self):
        """"""
        self.client.login(username='admin', password='admin')
        response = self.client.get('/plot-id-1/membership/')
        self.assertEqual(response.status_code, 404)
    
    def test_membership_page_url_by_chairman_user(self):
        """"""
        self.client.login(username='chairman2', password='pswd2000')
        response = self.client.get('/plot-id-1/membership/')
        self.assertEqual(response.status_code, 404)

    def test_membership_page_url_by_accountant_user(self):
        """"""
        self.client.login(username='accountant2', password='pswd4000')
        response = self.client.get('/plot-id-1/membership/')
        self.assertEqual(response.status_code, 404)

    def test_membership_page_url_by_true_owner_user(self):
        """Test owner access to his membership data."""
        self.client.login(username='owner1', password='pswd5000')
        response = self.client.get('/plot-id-1/membership/')
        self.assertEqual(response.status_code, 200)

    def test_membership_page_url_by_fake_owner_user(self):
        """Test owner access to other owner membership data."""
        self.client.login(username='owner2', password='pswd6000')
        response = self.client.get('/plot-id-1/membership/')
        self.assertEqual(response.status_code, 404)

    # Test URLconf name and template
    def test_membership_page_url_conf_name(self):
        """"""
        self.client.login(username='owner1', password='pswd5000')
        response = self.client.get(reverse('membership', kwargs={'plot_id': 1}))
        self.assertEqual(response.status_code, 200)

    def test_membership_page_template(self):
        """"""
        self.client.login(username='owner1', password='pswd5000')
        response = self.client.get('/plot-id-1/membership/')
        self.assertTemplateUsed(response, 'membership_payments_page.html')

    # Test context content and data
    def test_membership_page_context_keys(self):
        """Test all content[keys] exist in response."""
        self.client.login(username='owner1', password='pswd5000')
        response = self.client.get('/plot-id-1/membership/')
        self.assertIn('snt_list', response.context)
        self.assertIn('auth_form', response.context)
        self.assertIn('user_name', response.context)
        self.assertIn('land_plots', response.context)
        self.assertIn('land_plot', response.context)
        self.assertIn('payment_data_list', response.context)

    def test_membership_page_context_data(self):
        """Verify context data is correct."""
        self.client.login(username='owner1', password='pswd5000')
        response = self.client.get('/plot-id-1/membership/')
        snt_list = Snt.objects.all()
        user = User.objects.filter(username__exact='owner1').get()
        user_name = Owner.objects.filter(
            user__exact=user).get()
        land_plots = LandPlot.objects.filter(
            owner__user__exact=user).all()
        land_plot_1 = LandPlot.objects.get(id=1)
        payment_data_list = MPayment.objects.filter(
            land_plot__exact=land_plot_1,
            ).order_by('-year_period')
        self.assertEqual(
            response.context['snt_list'][0],
            snt_list[0],
            )       
        self.assertEqual(
            response.context['auth_form'],
            AuthenticationForm,
            )
        self.assertEqual(
            response.context['user_name'],
            user_name.__str__(),
            )
        if len(response.context['land_plots']) > 0:
            for key, value in enumerate(response.context['land_plots']):
                self.assertEqual(
                    value,
                    land_plots[key],
                    )   
        self.assertEqual(
            response.context['land_plot'],
            LandPlot.objects.get(id=1),
            )
        if len(response.context['payment_data_list']) > 0:
            for key, value in enumerate(response.context['payment_data_list']):
                self.assertEqual(
                    value,
                    payment_data_list[key]
                    )
