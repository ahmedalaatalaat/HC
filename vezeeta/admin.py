from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *
# Register your models here.
admin.site.register(PhysicianPatientBooking)
admin.site.register(ClinicPatientBooking)
admin.site.register(HospitalPatientBooking)
@admin.register(PhysicianRecommendation)

class ViewAdmin(ImportExportModelAdmin):
	pass


