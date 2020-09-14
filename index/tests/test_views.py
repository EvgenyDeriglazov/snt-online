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

from django.test import TestCase, Client
from index.models import *
from django.contrib.auth.forms import AuthenticationForm

class TestHomePage(TestCase):
    """"""
    fixtures = ['test_db.json']
    # Test functions
    def test_home_page_url(self):
        """"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_home_page_url_conf_name(self):
        """"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_page_template(self):
        """"""
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home_page.html')

    def test_home_page_context_content(self):
        """Test all content[keys] exist in response."""
        response = self.client.get('')
        self.assertIn('snt_list', response.context)
        self.assertIn('land_plots_count', response.context)
        self.assertIn('auth_form', response.context)
        self.assertIn('user_name', response.context)
        self.assertIn('land_plots', response.context)

    def test_home_page_context_data(self):
        """Test context data."""
        response = self.client.get('')
        self.assertEqual(len(response.context['snt_list']), 1)

class TestInfoPage(TestCase):
    # Test functions
    def test_info_page_url(self):
        """"""
        response = self.client.get('/info/')
        self.assertEqual(response.status_code, 200)

    def test_info_page_url_conf_name(self):
        """"""
        response = self.client.get(reverse('info'))
        self.assertEqual(response.status_code, 200)


    def test_info_page_template(self):
        """"""
        response = self.client.get('/info/')
        self.assertTemplateUsed(response, 'info_page.html')

    def test_info_page_context_content(self):
        """Test dict keys exists."""
        response = self.client.get('/info/')
        self.assertIn('snt_list', response.context)
        self.assertIn('info_list', response.context)
        self.assertIn('auth_form', response.context)
        self.assertIn('user_name', response.context)
        self.assertIn('land_plots', response.context)

class TestInfoDetailsPage(TestCase):
    fixtures = ['test_db.json']

    # Test functions
    def test_info_details_page_url(self):
        """"""
        response = self.client.get('/info/1/')
        self.assertEqual(response.status_code, 200)

    def test_info_details_page_url_conf_name(self):
        """"""
        response = self.client.get(reverse('info-details', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)


    def test_info_details_page_template(self):
        """"""
        response = self.client.get('/info/1/')
        self.assertTemplateUsed(response, 'info_details_page.html')

    def test_info_details_page_context_content(self):
        """Test all content[keys] exist in response."""
        response = self.client.get('/info/1/')
        self.assertIn('info_details', response.context)
        self.assertIn('snt_list', response.context)
        self.assertIn('auth_form', response.context)
        self.assertIn('user_name', response.context)
        self.assertIn('land_plots', response.context)

class TestBankDetailsPage(TestCase):
    """"""
    #fixtures = ['test_db.json']

    # Test functions
    def test_bank_details_page_url(self):
        """"""
        response = self.client.get('/snt-bank-details/')
        self.assertEqual(response.status_code, 200)

    def test_bank_details_page_url_conf_name(self):
        """"""
        response = self.client.get(reverse('snt-bank-details'))
        self.assertEqual(response.status_code, 200)

    def test_bank_details_page_template(self):
        """"""
        response = self.client.get('/snt-bank-details/')
        self.assertTemplateUsed(response, 'snt_bank_details_page.html')

    def test_bank_details_page_context_content(self):
        """Test all content[keys] exist in response."""
        response = self.client.get('/snt-bank-details/')
        self.assertIn('snt_list', response.context)
        self.assertIn('auth_form', response.context)
        self.assertIn('user_name', response.context)
        self.assertIn('land_plots', response.context)

class TestSntContactsPage(TestCase):
    """"""
    fixtures = ['test_db.json']

    # Test functions
    def test_snt_contacts_page_url(self):
        """"""
        response = self.client.get('/contacts/')
        self.assertEqual(response.status_code, 200)

    def test_snt_contacts_page_url_conf_name(self):
        """"""
        response = self.client.get(reverse('snt-contacts'))
        self.assertEqual(response.status_code, 200)

    def test_snt_contacts_page_template(self):
        """"""
        response = self.client.get('/contacts/')
        self.assertTemplateUsed(response, 'snt_contacts_page.html')

    def test_snt_contacts_page_context_content(self):
        """Test all content[keys] exist in response."""
        response = self.client.get('/contacts/')
        self.assertIn('snt_list', response.context)
        self.assertIn('auth_form', response.context)
        self.assertIn('user_name', response.context)
        self.assertIn('chair_man', response.context)
        self.assertIn('accountant', response.context)
        self.assertIn('land_plots', response.context)

class TestDocsPage(TestCase):
    """"""
    fixtures = ['test_db.json']

    # Test functions
    def test_docs_page_url(self):
        """"""
        response = self.client.get('/docs/')
        self.assertEqual(response.status_code, 200)

    def test_docs_page_url_conf_name(self):
        """"""
        response = self.client.get(reverse('docs'))
        self.assertEqual(response.status_code, 200)

    def test_docs_page_template(self):
        """"""
        response = self.client.get('/docs/')
        self.assertTemplateUsed(response, 'docs_page.html')

    def test_docs_page_context_content(self):
        """Test all content[keys] exist in response."""
        response = self.client.get('/docs/')
        self.assertIn('snt_list', response.context)
        self.assertIn('docs_list', response.context)
        self.assertIn('auth_form', response.context)
        self.assertIn('user_name', response.context)
        self.assertIn('land_plots', response.context)
 
class TestDocsDetailsPage(TestCase):
    """"""
    fixtures = ['test_db.json']

    # Test functions
    def test_docs_details_page_url(self):
        """"""
        response = self.client.get('/docs/1/')
        self.assertEqual(response.status_code, 200)

    def test_docs_details_page_url_conf_name(self):
        """"""
        response = self.client.get(reverse('docs-details', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)

    def test_docs_details_page_template(self):
        """"""
        response = self.client.get('/docs/1/')
        self.assertTemplateUsed(response, 'docs_details_page.html')

    def test_docs_details_page_context_content(self):
        """Test all content[keys] exist in response."""
        response = self.client.get('/docs/1/')
        self.assertIn('snt_list', response.context)
        self.assertIn('docs_details', response.context)
        self.assertIn('auth_form', response.context)
        self.assertIn('user_name', response.context)
        self.assertIn('land_plots', response.context)
 
class TestLandPlotPage(TestCase):
    """LandPlotPage in Index app views."""
    fixtures = ['test_db.json']

    # Test functions
    def test_land_plot_page_url_by_unauthenticated_user(self):
        """"""
        response = self.client.get('/plot-id-1/')
        self.assertEqual(response.status_code, 302)

    def test_land_plot_page_url_by_super_user(self):
        """"""
        self.client.login(username='admin', password='admin')
        response = self.client.get('/plot-id-1/')
        self.assertEqual(response.status_code, 404)
    
    def test_land_plot_page_url_by_chairman_user(self):
        """"""
        self.client.login(username='chairman2', password='pswd2000')
        response = self.client.get('/plot-id-1/')
        self.assertEqual(response.status_code, 404)

    def test_land_plot_page_url_by_accountant_user(self):
        """"""
        self.client.login(username='accountant2', password='pswd4000')
        response = self.client.get('/plot-id-1/')
        self.assertEqual(response.status_code, 404)

    def test_land_plot_page_url_by_true_owner_user(self):
        """Test owner access to his land plot data."""
        self.client.login(username='owner1', password='pswd5000')
        response = self.client.get('/plot-id-1/')
        self.assertEqual(response.status_code, 200)

    def test_land_plot_page_url_by_fake_owner_user(self):
        """Test owner access to other owner land plot data."""
        self.client.login(username='owner2', password='pswd6000')
        response = self.client.get('/plot-id-1/')
        self.assertEqual(response.status_code, 404)

    def test_land_plot_page_url_conf_name(self):
        """"""
        self.client.login(username='owner1', password='pswd5000')
        response = self.client.get(reverse('land-plot', kwargs={'plot_id': 1}))
        self.assertEqual(response.status_code, 200)

    def test_land_plot_page_template(self):
        """"""
        self.client.login(username='owner1', password='pswd5000')
        response = self.client.get('/plot-id-1/')
        self.assertTemplateUsed(response, 'land_plot_page.html')

    def test_land_plot_page_context_content(self):
        """Test all content[keys] exist in response."""
        self.client.login(username='owner1', password='pswd5000')
        response = self.client.get('/plot-id-1/')
        self.assertIn('snt_list', response.context)
        self.assertIn('auth_form', response.context)
        self.assertIn('user_name', response.context)
        self.assertIn('land_plots', response.context)
        self.assertIn('land_plot', response.context)

    def test_land_plot_page_context_data(self):
        """Verify context data is correct."""
        self.client.login(username='owner1', password='pswd5000')
        response = self.client.get('/plot-id-1/')
        snt_list = Snt.objects.all()
        user = User.objects.filter(username__exact='owner1').get()
        user_name = Owner.objects.filter(
            user__exact=user).get()
        land_plots = LandPlot.objects.filter(
            owner__user__exact=user).all()
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

