from django.forms import ModelForm, HiddenInput
from membership.models import *

class NoFieldsMPaymentForm(ModelForm):
	"""MPayment form without fields to call model methods."""
	class Meta:
		model = MPayment
		fields = []

class NoFieldsTPaymentForm(ModelForm):
    """TPayment form without fields to call model methods."""
    class Meta:
        model = TPayment
        fields = []
