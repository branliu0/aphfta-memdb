from django.contrib import admin
from models import Facility

class FacilityAdmin(admin.ModelAdmin):
  list_display = ('facility_name', 'doctor_ic', 'tel_office', 'email', 'region', 'district', 'membership_type', 'membership')
  search_fields = ('facility_name', 'doctor_ic', 'tel_office', 'moh_reg_cert', 'email')
  list_filter = ('membership_type', 'region', 'district')
  date_hierarchy = 'date_joined'
  ordering = ('facility_name',)

admin.site.register(Facility, FacilityAdmin)
