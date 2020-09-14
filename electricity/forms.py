from django.forms import ModelForm, HiddenInput
from electricity.models import *

class CreateSingleECounterRecordForm(ModelForm):
    """Form to create new ECounterRecord for single type
    electrical counter model."""
    class Meta:
        model = ECounterRecord
        exclude = ['t1', 't2']
        #fields = '__all__'#['s']
        widgets = {
        	'land_plot': HiddenInput(),
        	'e_counter': HiddenInput(),
        	}

class CreateDoubleECounterRecordForm(ModelForm):
    """Form to create new ECounterRecord for double type
    electrical counter model."""
    class Meta:
        model = ECounterRecord
        exclude = ['s']
        widgets = {
        	'land_plot': HiddenInput(),
        	'e_counter': HiddenInput(),
        	}
        	
class CreateEPaymentForm(ModelForm):
	"""From to create EPayment based on ECounterRecord."""
	class Meta:
		model = ECounterRecord
		fields = []

class DeleteECounterRecordForm(ModelForm):
	"""Form to delete ECounterRecord from db."""
	class Meta:
		model = ECounterRecord
		fields = []

class NoFieldsEPaymentForm(ModelForm):
	"""EPayment form without fields to call model methods."""
	class Meta:
		model = EPayment
		fields = []
