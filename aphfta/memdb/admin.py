from django.contrib import admin
from models import Facility, Program
from helpers.filters import (makeSelectFilter, makeBooleanSelectFilter,
                             makeMultiselectFilter)


class FacilityAdmin(admin.ModelAdmin):
  list_display = ('facility_name', 'doctor_ic', 'full_contact', 'region', 'district', 'membership_type', 'membership')
  list_editable = ('doctor_ic', )
  search_fields = ('facility_name', 'doctor_ic', 'tel_office', 'moh_reg_cert', 'email')
  list_filter = (
      makeSelectFilter('membership_type'),
      makeSelectFilter('region'),
      makeSelectFilter('district'),
      makeSelectFilter('zone'),
      makeBooleanSelectFilter('lab'),
      makeBooleanSelectFilter('xray'),
      makeBooleanSelectFilter('blood_bank'),
      makeBooleanSelectFilter('pharmacy'),
      makeBooleanSelectFilter('dental'),
      makeBooleanSelectFilter('ultrasonography'),
      makeBooleanSelectFilter('icu'),
      makeBooleanSelectFilter('ambulance'),
  )
  filter_horizontal = ('programs',)
  ordering = ('facility_name',)

  class Media:
    css = {
      'all': ('css/chosen.css',)
    }
    js = ('scripts/jquery-1.8.3.min.js',
          'scripts/chosen.jquery.min.js')

admin.site.register(Facility, FacilityAdmin)
admin.site.register(Program)
