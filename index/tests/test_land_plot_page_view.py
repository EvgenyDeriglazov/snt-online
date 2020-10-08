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
        self.assertEqual(
            response.context['exception'],
            "Такой страницы не существует"
            )

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

    def test_land_plot_page_context_keys(self):
        """Test context dict keys."""
        self.client.login(username='owner1', password='pswd5000')
        response = self.client.get('/plot-id-1/')
        self.assertIn('snt_list', response.context)
        self.assertIn('auth_form', response.context)
        self.assertIn('user_name', response.context)
        self.assertIn('land_plots', response.context)
        self.assertIn('land_plot', response.context)

    def test_land_plot_page_context_values(self):
        """Test context dict values."""
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
