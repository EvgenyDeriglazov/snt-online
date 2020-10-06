from django.contrib import admin
from .models import *

# Register your models here.
#admin.site.register(Docs)
#admin.site.register(Info)

@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
	list_display = (
		'__str__', 'user', 'join_date', 'leave_date', 'phone', 'email',
		)
	list_filter = ('leave_date', 'user__is_active')
	
@admin.register(LandPlot)
class LandPlotAdmin(admin.ModelAdmin):
    list_display = (
		'plot_number', 'plot_area', 'owner', 'user_name',
		)
    ordering = ['plot_number']
    def user_name(self, obj):
        return obj.owner.user

    user_name.short_description = "логин"

@admin.register(ChairMan)
class ChairManAdmin(admin.ModelAdmin):
    list_display = (
        '__str__', 'user', 'join_date', 'leave_date', 'phone', 'email',
        )
    list_filter = ('leave_date', 'user__is_active')

@admin.register(Accountant)
class AccountantAdmin(admin.ModelAdmin):
    list_display = (
        '__str__', 'user', 'join_date', 'leave_date', 'phone', 'email',
        )
    list_filter = ('leave_date', 'user__is_active')

@admin.register(Snt)
class SntAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'personal_acc', 'bank_name', 'bic', 'corresp_acc', 'inn',
        'kpp', 'address', 'chair_man',
        )
