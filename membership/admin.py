from django.contrib import admin
from .models import *

# Register your models here.
#admin.site.register(MPayment)
#admin.site.register(MRate)
#admin.site.register(TPayment)

@admin.register(MRate)
class MRateAdmin(admin.ModelAdmin):
    list_display = (
        'period', 'date', 'period_rate',
        )
    list_filter = ('year_period',)
    ordering = ['-year_period', 'month_period']

    def period(self, obj):
        return obj.year_period + ' ' + obj.get_month_period_display()
    period.short_description = "период"

    def period_rate(self, obj):
        return obj.rate
    period_rate.short_descrition = "размер взноса за сотку"

@admin.register(MPayment)
class MPaymentAdmin(admin.ModelAdmin):
    list_display = (
        'period', 'land_plot', 'payment_date', 'status', 'amount',
        )

    list_filter = ('status', 'year_period',)
    ordering = ['-year_period', 'month_period']

    def period(self, obj):
        return obj.year_period + ' ' + obj.get_month_period_display()
    period.short_description = "период"

@admin.register(TPayment)
class TPaymentAdmin(admin.ModelAdmin):
    list_display = (
    'target', 'land_plot', 'payment_date', 'status', 'amount',
    )
    list_filter = ('status', 'target')
    ordering =['payment_date']
