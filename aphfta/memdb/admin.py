from django.contrib import admin
from models import Facility, Program
from helpers.admin_filters import SelectFilter, BooleanSelectFilter, M2MSelectFilter


class FacilityAdmin(admin.ModelAdmin):
  list_display = ('facility_name', 'doctor_ic', 'full_contact', 'address', 'region', 'district', 'zone', 'programs_list', 'membership')
  search_fields = ('facility_name', 'doctor_ic', 'tel_office', 'moh_reg_cert', 'email')
  list_filter = (
      SelectFilter('membership_type'),
      SelectFilter('region'),
      SelectFilter('district'),
      SelectFilter('zone'),
      M2MSelectFilter('programs', 'name'),
      BooleanSelectFilter('lab'),
      BooleanSelectFilter('xray'),
      BooleanSelectFilter('blood_bank'),
      BooleanSelectFilter('pharmacy'),
      BooleanSelectFilter('dental'),
      BooleanSelectFilter('ultrasonography'),
      BooleanSelectFilter('icu'),
      BooleanSelectFilter('ambulance'),
  )
  filter_horizontal = ('programs',)
  ordering = ('facility_name',)
  save_on_top = True

  class Media:
    css = {
      'all': ('css/chosen.css',)
    }
    js = ('scripts/jquery-1.8.3.min.js',
          'scripts/chosen.jquery.min.js')

class ProgramAdmin(admin.ModelAdmin):
  list_display = ('name', 'description')

admin.site.register(Facility, FacilityAdmin)
admin.site.register(Program, ProgramAdmin)
