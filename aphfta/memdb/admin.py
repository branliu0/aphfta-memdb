from django.contrib import admin
from models import Facility
from helpers.filters import makeSelectFilter, makeBooleanSelectFilter


class FacilityAdmin(admin.ModelAdmin):
  list_display = ('facility_name', 'doctor_ic', 'full_contact', 'region', 'district', 'membership_type', 'membership', 'edit_balance')
  list_editable = ('doctor_ic', )
  search_fields = ('facility_name', 'doctor_ic', 'tel_office', 'moh_reg_cert', 'email')
  list_filter = (
      makeSelectFilter('membership_type'),
      makeSelectFilter('region'),
      makeSelectFilter('district'),
      makeBooleanSelectFilter('lab'),
      makeBooleanSelectFilter('xray'),
      makeBooleanSelectFilter('blood_bank'),
      makeBooleanSelectFilter('pharmacy'),
      makeBooleanSelectFilter('dental'),
      makeBooleanSelectFilter('ultrasonography'),
      makeBooleanSelectFilter('icu'),
      makeBooleanSelectFilter('ambulance'),
  )
  ordering = ('facility_name',)

  def edit_balance(self, obj):
    if obj.balance == 0:
        return '<a class="paid balance" href="http://www.yahoo.com">Paid</a>'
    return '<a class="balance" href="http://www.google.com">%s</a>' % obj.balance
  edit_balance.allow_tags = True



admin.site.register(Facility, FacilityAdmin)
