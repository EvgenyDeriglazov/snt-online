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
from membership.forms import *
import datetime
import json

# response is a TemplateResponse object

@tag('views', 'membership', 'membership-views')
class TargetPaymentDetailsPage(TestCase):
    """TargetPaymentDetailsPage in Membership app view."""
    fixtures = ['test_db.json']
    @classmethod
    def setUpTestData(cls):
        t_payment = TPayment.objects.create(
            target="test",
            amount=5000,
            land_plot=LandPlot.objects.get(id=1),
            )

    # Test URL access
    def test_target_details_page_url_by_unauthenticated_user(self):
        """"""
        response = self.client.get('/plot-id-1/membership/t-payment-id-1/')
        self.assertEqual(response.status_code, 302)

    def test_target_details_page_url_by_super_user(self):
        """"""
        self.client.login(username='admin', password='admin')
        response = self.client.get('/plot-id-1/membership/t-payment-id-1/')
        self.assertEqual(response.status_code, 404)
    
    def test_target_details_page_url_by_chairman_user(self):
        """"""
        self.client.login(username='chairman2', password='pswd2000')
        response = self.client.get('/plot-id-1/membership/t-payment-id-1/')
        self.assertEqual(response.status_code, 404)

    def test_target_details_page_url_by_accountant_user(self):
        """"""
        self.client.login(username='accountant2', password='pswd4000')
        response = self.client.get('/plot-id-1/membership/t-payment-id-1/')
        self.assertEqual(response.status_code, 404)

    def test_target_details_page_url_by_true_owner_user(self):
        """Test owner access to his membership data."""
        self.client.login(username='owner1', password='pswd5000')
        response = self.client.get('/plot-id-1/membership/t-payment-id-1/')
        self.assertEqual(response.status_code, 200)

    def test_target_details_page_url_by_fake_owner_user(self):
        """Test owner access to other owner membership data."""
        self.client.login(username='owner2', password='pswd6000')
        response = self.client.get('/plot-id-1/membership/t-payment-id-1/')
        self.assertEqual(response.status_code, 404)

    # Test URLconf name and template
    def test_target_details_page_url_conf_name(self):
        """"""
        self.client.login(username='owner1', password='pswd5000')
        response = self.client.get(
            reverse(
                'target-payment-details',
                kwargs={'plot_id': 1, 't_payment_id': 1}
                )
            )
        self.assertEqual(response.status_code, 200)

    def test_by_args_target_details_page_url_conf_name(self):
        """"""
        self.client.login(username='owner1', password='pswd5000')
        response = self.client.get(
            reverse(
                'target-payment-details',
                args=[1, 1]
                )
            )
        self.assertEqual(response.status_code, 200)

    # Test template
    def test_target_details_page_template(self):
        """"""
        self.client.login(username='owner1', password='pswd5000')
        response = self.client.get('/plot-id-1/membership/t-payment-id-1/')
        self.assertTemplateUsed(response, 'target_payment_details_page.html')

    # Test POST method to set MPayment.status = 'paid'.
    def test_target_details_page_post_method(self):
        """TPayment model paid() method."""
        self.assertEqual(
            TPayment.objects.filter(id=1, status__exact='paid').exists(),
            False
            )       
        self.client.login(username='owner1', password='pswd5000')
        response = self.client.post(
            '/plot-id-1/membership/t-payment-id-1/',
            follow=True,
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            TPayment.objects.filter(id=1, status__exact='paid').exists(),
            True
            )
        
    # Test context content and data
    def test_target_details_page_context_keys(self):
        """Test all content[keys] exist in response."""
        self.client.login(username='owner1', password='pswd5000')
        response = self.client.get('/plot-id-1/membership/t-payment-id-1/')
        self.assertIn('snt_list', response.context)
        self.assertIn('auth_form', response.context)
        self.assertIn('user_name', response.context)
        self.assertIn('land_plots', response.context)
        self.assertIn('land_plot', response.context)
        self.assertIn('t_payment', response.context)
        self.assertIn('qr_pay_data', response.context)
        self.assertIn('form', response.context)

    def test_target_details_page_context_values(self):
        """Verify context data is correct."""
        self.client.login(username='owner1', password='pswd5000')
        response = self.client.get('/plot-id-1/membership/t-payment-id-1/')
        snt_list = Snt.objects.all()
        user = User.objects.filter(username__exact='owner1').get()
        user_name = Owner.objects.filter(
            user__exact=user).get()
        land_plots = LandPlot.objects.filter(
            owner__user__exact=user).all()
        land_plot_1 = LandPlot.objects.get(id=1)

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
        self.assertEqual(
            response.context['t_payment'],
            TPayment.objects.get(id=1),
            )
        self.assertIsInstance(
            response.context['form'],
            NoFieldsTPaymentForm,
            )
