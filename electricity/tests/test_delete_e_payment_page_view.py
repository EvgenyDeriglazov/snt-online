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
# use commands below (choose one of 2)
# python3 manage.py dumpdata -e contenttypes -e auth.Permission  > test_db.json
# python3 manage.py dumpdata --indent 4 --exclude contenttypes --format json >
# test_db.json
# then move the json file to appname.fixtures directory

from django.test import TestCase, Client, tag
from index.models import *
from electricity.models import *
from django.contrib.auth.forms import AuthenticationForm
from electricity.views import e_counter, all_e_counter_records
from electricity.views import e_counter_records_with_e_payments_list
from electricity.views import create_e_counter_record_form
from electricity.forms import *
import datetime
import json

# response is a TemplateResponse object

@tag('views', 'electricity', 'electricity-views')
class DeleteEPaymentPage(TestCase):
    """"""
    fixtures = ['test_db.json']

    # Test URL access
    def test_pay_e_payment_page_url_by_unauthenticated_user(self):
        """Test unauthenticated user access to owner user data."""
        response = self.client.get('/plot-id-1/electricity/e-payment-id-3/delete/')
        self.assertEqual(response.status_code, 302)

    def test_pay_e_payment_page_url_by_super_user(self):
        """Test super user access to owner user data."""
        self.client.login(username='admin', password='admin')
        response = self.client.get('/plot-id-1/electricity/e-payment-id-3/delete/')
        self.assertEqual(response.status_code, 404)
    
    def test_pay_e_payment_page_url_by_chairman_user(self):
        """Test chairman user access to owner user data."""
        self.client.login(username='chairman2', password='pswd2000')
        response = self.client.get('/plot-id-1/electricity/e-payment-id-3/delete/')
        self.assertEqual(response.status_code, 404)

    def test_pay_e_payment_page_url_by_accountant_user(self):
        """Test accountant user access to owner user data."""
        self.client.login(username='accountant2', password='pswd4000')
        response = self.client.get('/plot-id-1/electricity/e-payment-id-3/delete/')
        self.assertEqual(response.status_code, 404)

    def test_pay_e_payment_page_url_by_true_owner_user(self):
        """Test owner access to his record details data."""
        self.client.login(username='owner1', password='pswd5000')
        response = self.client.get('/plot-id-1/electricity/e-payment-id-3/delete/')
        self.assertEqual(response.status_code, 200)

    def test_pay_e_payment_page_url_by_fake_owner_user(self):
        """Test owner access to other owner electricity data."""
        self.client.login(username='owner2', password='pswd6000')
        response = self.client.get('/plot-id-1/electricity/e-payment-id-3/delete/')
        self.assertEqual(response.status_code, 404)

    # Test URLconf name and template
    def test_pay_e_payment_page_url_conf_name(self):
        """"""
        self.client.login(username='owner1', password='pswd5000')
        response = self.client.get(
            reverse(
                'delete-e-payment',
                kwargs={'plot_id': 1, 'e_payment_id': 3}
                )
            )
        self.assertEqual(response.status_code, 200)

    def test_pay_e_payment_page_template(self):
        """"""
        self.client.login(username='owner1', password='pswd5000')
        response = self.client.get('/plot-id-1/electricity/e-payment-id-3/delete/')
        self.assertTemplateUsed(response, 'delete_e_payment_page.html')

    def test_by_args_del_e_payment_page_url_conf_name(self):
        """"""
        self.client.login(username='owner1', password='pswd5000')
        response = self.client.get(
            reverse(
                'delete-e-payment',
                args=[1, 3]
                )
            )
        self.assertEqual(response.status_code, 200)

    # Test POST method
    def test_del_e_payment_post_method(self):
        """Submit the form to server."""
        # response is a TemplateResponse object
        self.client.login(username='owner1', password='pswd5000')
        response = self.client.post(
            '/plot-id-1/electricity/e-payment-id-3/delete/',
            follow=True
            )
        self.assertEqual(response.status_code, 200)
        # Check that e_payment was deleted
        self.assertEqual(EPayment.objects.filter(id=3).exists(), False)
        response = self.client.get('/plot-id-1/electricity/e-payment-id-3/')
        self.assertEqual(response.status_code, 404)
        response = self.client.get('/plot-id-1/electricity/e-payment-id-3/delete/')
        self.assertEqual(response.status_code, 404)

    # Test context content and data
    def test_pay_e_payment_page_context_content(self):
        """Test all content[keys] exist in response."""
        self.client.login(username='owner1', password='pswd5000')
        response = self.client.get('/plot-id-1/electricity/e-payment-id-3/delete/')
        self.assertIn('snt_list', response.context)
        self.assertIn('auth_form', response.context)
        self.assertIn('user_name', response.context)
        self.assertIn('land_plots', response.context)
        self.assertIn('land_plot', response.context)
        self.assertIn('counter_type', response.context)
        self.assertIn('record', response.context)
        self.assertIn('e_payment', response.context)
        self.assertIn('form', response.context)

    def test_pay_e_payment_page_context_data(self):
        """Verify context data is correct."""
        self.client.login(username='owner1', password='pswd5000')
        response = self.client.get('/plot-id-1/electricity/e-payment-id-3/delete/')
        snt_list = Snt.objects.all()
        record = ECounterRecord.objects.get(id=3)
        user = User.objects.filter(username__exact='owner1').get()
        user_name = Owner.objects.filter(
            user__exact=user).get()
        land_plots = LandPlot.objects.filter(
            owner__user__exact=user).all()
        counter_type = record.e_counter.model_type
        e_payment = record.epayment
        form = NoFieldsEPaymentForm()

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
        self.assertEqual(
            response.context['land_plots'][0],
            land_plots[0],
            )       
        self.assertEqual(
            response.context['land_plots'][1],
            land_plots[1],
            )       
        self.assertEqual(
            response.context['land_plot'],
            LandPlot.objects.get(id=1),
            )
        self.assertEqual(
            response.context['counter_type'],
            counter_type
            )
        self.assertEqual(
            response.context['record'],
            record,
            )
        self.assertEqual(
            response.context['e_payment'],
            e_payment,
            )
        self.assertIsInstance(
            response.context['form'],
            NoFieldsEPaymentForm,
            )