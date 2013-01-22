from django.contrib import admin
from models import Facility, Fee, Payment
from helpers.filters import makeSelectFilter, makeBooleanSelectFilter


class FacilityAdmin(admin.ModelAdmin):
  list_display = ('facility_name', 'doctor_ic', 'full_contact', 'region', \
                  'district', 'membership_type', 'membership', 'edit_balance')
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
    if obj.balance() == 0:
        return '<a class="paid balance" data-id="{0}" href="#">Paid</a>'.format(obj.id)
    return '<a class="balance" data-id="{0}" href="#">{1}</a>'.format(obj.id, obj.balance())
  edit_balance.allow_tags = True

class FeeAdmin(admin.ModelAdmin):
  list_display = ('name', 'year', 'type', 'amount')
  search_fields = ('name', 'year', 'type', 'amount')

  filter_horizontal = ("facility",)

  '''
    This was originally meant for when you you could either add all regions in a clinic, or add individual clinics,
    now you can do both at the same time

  def save_related(self, request, form, formsets, change):
    if request.POST.get('region'):
      post = request.POST.dict()
      for facility in Facility.objects.filter(region__iexact=request.POST.get('region')):
        facility.fee_set.add(self.latest_fee)

  def save_model(self, request, obj, form, change):
    self.latest_fee = obj
    # alteredPOST = request.POST.copy()
    # if not request.POST.get('facility'):
      # for facility in Facility.objects.filter(region__iexact=request.POST.get('region')):
        # obj.facility.add(facility)

    obj.save()
  '''

  def clean_facility(self):
    print "hey there"

  @staticmethod
  def getName():
    return "Fee"

  @staticmethod
  def getRegions():
    return map(lambda x: x['region'], Facility.objects.values('region').distinct())

class PaymentAdmin(admin.ModelAdmin):
  list_display = ('facility', 'date', 'amount')
  search_display = ('facility', 'date', 'amount')


admin.site.register(Facility, FacilityAdmin)
admin.site.register(Fee, FeeAdmin)
admin.site.register(Payment, PaymentAdmin)
