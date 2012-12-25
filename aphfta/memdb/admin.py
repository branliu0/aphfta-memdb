from django.contrib import admin
from models import Facility, OtherStaff, Ward

class FacilityAdmin(admin.ModelAdmin):
  list_display = ('facility_name', 'doctor_ic', 'tel_office', 'email', 'moh_reg_cert')
  search_fields = ('facility_name', 'tel_office', 'moh_reg_cert')
  date_hierarchy = 'date_joined'
  ordering = ('facility_name',)

admin.site.register(Facility, FacilityAdmin)
admin.site.register(OtherStaff)
admin.site.register(Ward)
