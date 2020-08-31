from django.forms import ModelForm
from electricity.models import *

class NewECounterRecordForm(ModelForm):
    """Form to create new ECounterRecord."""
    class Meta:
        model = ECounterRecord
        fields = ['s', 't1', 't2']
