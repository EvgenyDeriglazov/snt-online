from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(ECounter)
admin.site.register(ECounterRecord)
admin.site.register(ERate)
admin.site.register(EPayment)
