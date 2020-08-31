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

from django.test import TestCase, Client
from index.models import *
from electricity.models import *
from django.contrib.auth.forms import AuthenticationForm
from electricity.views import e_counter, all_e_counter_records
from electricity.views import e_counter_records_with_e_payments_list

class ElectricityPage(TestCase):
    """ElectriciyPage in Electricity app view."""
    fixtures = ['test_db.json']

    # Test URL access
    def test_electricity_page_url_by_unauthenticated_user(self):
        """"""
        response = self.client.get('/plot-id-1/electricity/')
        self.assertEqual(response.status_code, 302)

    def test_electricity_page_url_by_super_user(self):
        """"""
        self.client.login(username='admin', password='admin')
        response = self.client.get('/plot-id-1/electricity/')
        self.assertEqual(response.status_code, 404)
    
    def test_electricity_page_url_by_chairman_user(self):
        """"""
        self.client.login(username='chairman2', password='pswd2000')
        response = self.client.get('/plot-id-1/electricity/')
        self.assertEqual(response.status_code, 404)

    def test_electricity_page_url_by_accountant_user(self):
        """"""
        self.client.login(username='accountant2', password='pswd4000')
        response = self.client.get('/plot-id-1/electricity/')
        self.assertEqual(response.status_code, 404)

    def test_electricity_page_url_by_true_owner_user(self):
        """Test owner access to his electricity data."""
        self.client.login(username='owner1', password='pswd5000')
        response = self.client.get('/plot-id-1/electricity/')
        self.assertEqual(response.status_code, 200)

    def test_electricity_page_url_by_fake_owner_user(self):
        """Test owner access to other owner electricity data."""
        self.client.login(username='owner2', password='pswd6000')
        response = self.client.get('/plot-id-1/electricity/')
        self.assertEqual(response.status_code, 404)

    # Test URLconf name and template

    def test_electricity_page_url_conf_name(self):
        """"""
        self.client.login(username='owner1', password='pswd5000')
        response = self.client.get(reverse('electricity', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)

    def test_electricity_page_template(self):
        """"""
        self.client.login(username='owner1', password='pswd5000')
        response = self.client.get('/plot-id-1/electricity/')
        self.assertTemplateUsed(response, 'electricity_page.html')

    # Test context content and data
    def test_electricity_page_context_content(self):
        """Test all content[keys] exist in response."""
        self.client.login(username='owner1', password='pswd5000')
        response = self.client.get('/plot-id-1/electricity/')
        self.assertIn('snt_list', response.context)
        self.assertIn('auth_form', response.context)
        self.assertIn('user_name', response.context)
        self.assertIn('land_plots', response.context)
        self.assertIn('land_plot', response.context)
        self.assertIn('e_counter', response.context)
        self.assertIn('payment_data_list', response.context)

    def test_electricity_page_context_data(self):
        """Verify context data is correct."""
        self.client.login(username='owner1', password='pswd5000')
        response = self.client.get('/plot-id-1/electricity/')
        snt_list = Snt.objects.all()
        user = User.objects.filter(username__exact='owner1').get()
        user_name = Owner.objects.filter(
            user__exact=user).get()
        land_plots = LandPlot.objects.filter(
            owner__user__exact=user).all()
        land_plot_1 = LandPlot.objects.get(id=1)
        e_counter_obj = land_plot_1.ecounter
        #e_counter_obj = e_counter(land_plot_1)
        payment_data_list = e_counter_records_with_e_payments_list(
            e_counter_obj,
            land_plot_1
            )
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
        	response.context['e_counter'],
        	e_counter_obj
            )
        self.assertEqual(
            response.context['payment_data_list'],
            payment_data_list
            )

    # Test helper functions
    def test_e_counter_method(self):
        """Test for helper function e_counter()."""
        land_plot_1 = LandPlot.objects.get(id=1)
        e_counter_obj = land_plot_1.ecounter
        self.assertEqual(
            e_counter(land_plot_1),
            e_counter_obj
            )

    def test_all_e_counter_records_method(self):
        """Test for helper function all_e_counter_records()."""
        land_plot_1 = LandPlot.objects.get(id=1)
        e_counter_obj = land_plot_1.ecounter 
        e_counter_records_list = ECounterRecord.objects.filter(
            e_counter__exact=e_counter_obj,
            land_plot__exact=land_plot_1,
            ).order_by('rec_date')
        test = all_e_counter_records(e_counter_obj, land_plot_1)
        for i, _ in enumerate(e_counter_records_list):
            self.assertEqual(
                test[i],
                e_counter_records_list[i]
                )

    def e_counter_records_with_e_payments_list_method(self):
        """Test for helper function
        e_coutner_records_with_e_payemnts_list()."""
        # Test result with data
        land_plot_1 = LandPlot.objects.get(id=1)
        e_counter_obj = land_plot_1.ecounter 
        payment_data_list = e_counter_records_with_e_payments_list(
            e_counter_obj, land_plot_1
            )
        e_counter_records_list = all_e_counter_records(e_counter, land_plot)
        if len(e_counter_records_list) > 0:
            list_of_lists = []
            for i in e_counter_records_list:
                list_item = [i]
                try:
                    list_item.append(i.epayment)
                except ECounterRecord.epayment.RelatedObjectDoesNotExist:
                    list_item.append(None)
                list_of_lists.append(list_item)
        else:
            list_of_lists = [[None, None]]
        self.assertEqual(payment_data_list, list_of_lists)
        # Test result without data
        land_plot_4 = LandPlot.objects.get(id=4)
        e_counter_obj = land_plot_4.ecounter 
        payment_data_list = e_counter_records_with_e_payments_list(
            e_counter_obj, land_plot_4
            )
        self.assertEqual(payment_data_list, [[None, None]])

class ECounterRecordDetailsPage(TestCase):
    """ECounterRecordDetailsPage in Electricity app views."""
    fixtures = ['test_db.json']

    # Test URL access
    def test_record_details_page_url_by_unauthenticated_user(self):
        """Test unauthenticated user access to owner user data."""
        response = self.client.get('/plot-id-1/electricity/record-id-1')
        self.assertEqual(response.status_code, 302)

    def test_record_details_page_url_by_super_user(self):
        """Test super user access to owner user data."""
        self.client.login(username='admin', password='admin')
        response = self.client.get('/plot-id-1/electricity/record-id-1')
        self.assertEqual(response.status_code, 404)
    
    def test_record_details_page_url_by_chairman_user(self):
        """Test chairman user access to owner user data."""
        self.client.login(username='chairman2', password='pswd2000')
        response = self.client.get('/plot-id-1/electricity/record-id-1')
        self.assertEqual(response.status_code, 404)

    def test_record_details_page_url_by_accountant_user(self):
        """Test accountant user access to owner user data."""
        self.client.login(username='accountant2', password='pswd4000')
        response = self.client.get('/plot-id-1/electricity/record-id-1')
        self.assertEqual(response.status_code, 404)

    def test_record_details_page_url_by_true_owner_user(self):
        """Test owner access to his record details data."""
        self.client.login(username='owner1', password='pswd5000')
        response = self.client.get('/plot-id-1/electricity/record-id-1')
        self.assertEqual(response.status_code, 200)

    def test_record_details_page_url_by_fake_owner_user(self):
        """Test owner access to other owner electricity data."""
        self.client.login(username='owner2', password='pswd6000')
        response = self.client.get('/plot-id-1/electricity/record-id-1')
        self.assertEqual(response.status_code, 404)

    # Test URLconf name and template
    def test_record_details_page_url_conf_name(self):
        """"""
        self.client.login(username='owner1', password='pswd5000')
        response = self.client.get(
            reverse(
                'e-counter-record-details',
                kwargs={'pk': 1, 'record_id': 1}
                )
            )
        self.assertEqual(response.status_code, 200)

    def test_record_details_page_template(self):
        """"""
        self.client.login(username='owner1', password='pswd5000')
        response = self.client.get('/plot-id-1/electricity/record-id-1')
        self.assertTemplateUsed(response, 'e_counter_record_details_page.html')

    def test2_record_details_page_url_conf_name(self):
        """"""
        self.client.login(username='owner1', password='pswd5000')
        response = self.client.get(
            reverse(
                'e-counter-record-details',
                args=[1, 1]
                )
            )
        self.assertEqual(response.status_code, 200)

    # Test context content and data
    def test_record_details_page_context_content(self):
        """Test all content[keys] exist in response."""
        self.client.login(username='owner1', password='pswd5000')
        response = self.client.get('/plot-id-1/electricity/record-id-1')
        self.assertIn('snt_list', response.context)
        self.assertIn('auth_form', response.context)
        self.assertIn('user_name', response.context)
        self.assertIn('land_plots', response.context)
        self.assertIn('land_plot', response.context)
        self.assertIn('counter_type', response.context)
        self.assertIn('record', response.context)

    def test_record_details_page_context_data(self):
        """Verify context data is correct."""
        self.client.login(username='owner1', password='pswd5000')
        response = self.client.get('/plot-id-1/electricity/record-id-1')
        snt_list = Snt.objects.all()
        record = ECounterRecord.objects.get(id=1)
        user = User.objects.filter(username__exact='owner1').get()
        user_name = Owner.objects.filter(
            user__exact=user).get()
        land_plots = LandPlot.objects.filter(
            owner__user__exact=user).all()
        land_plot_1 = LandPlot.objects.get(id=1)
        counter_type = record.e_counter.model_type

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