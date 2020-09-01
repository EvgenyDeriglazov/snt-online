from django.forms import ModelForm
from electricity.models import *

class NewSingleECounterRecordForm(ModelForm):
    """Form to create new ECounterRecord for single type
    electrical counter model."""
    class Meta:
        model = ECounterRecord
        fields = '__all__'#['s']

class NewDoubleECounterRecordForm(ModelForm):
    """Form to create new ECounterRecord for double type
    electrical counter model."""
    class Meta:
        model = ECounterRecord
        fields = ['t1', 't2']