from django.contrib import admin
from .models import *

# Register your models here.
#admin.site.register(ECounter)
#admin.site.register(ECounterRecord)
#admin.site.register(ERate)
#admin.site.register(EPayment)

@admin.register(ECounter)
class ECounterAdmin(admin.ModelAdmin):
    list_display = (
        'model_name', 'land_plot', 'reg_date', 'sn', 'model_type',
        )
    list_filter = ('model_type',)
    ordering = ['land_plot']

@admin.register(ERate)
class ERateAdmin(admin.ModelAdmin):
    list_display = (
        'date', 'snt', 's', 't1', 't2',
        )
    ordering = ['-date']

@admin.register(ECounterRecord)
class ECounterRecord(admin.ModelAdmin):
    list_display = (
        'rec_date', 'land_plot', 'e_counter', 's', 't1', 't2',
        )
    list_filter = ('land_plot',)
    ordering = ['-rec_date']

@admin.register(EPayment)
class EPaymentAdmin(admin.ModelAdmin):
    list_display = (
        'payment_date', 'land_plot', 'status', 'sum_total', 
        )
    list_filter = ('status', 'land_plot')
    ordering = ['-payment_date']
