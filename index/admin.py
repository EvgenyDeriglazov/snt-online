from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Snt)
#admin.site.register(LandPlot)
admin.site.register(ChairMan)
#admin.site.register(Owner)
admin.site.register(Accountant)
admin.site.register(Docs)
admin.site.register(Info)

@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
	list_display = (
		'__str__', 'user', 'join_date', 'leave_date',
		)
	list_filter = ('leave_date',)
	
@admin.register(LandPlot)
class LandPlotAdmin(admin.ModelAdmin):
	list_display = (
		'plot_number', 'plot_area', 'owner',
		)
	ordering = ['plot_number']
