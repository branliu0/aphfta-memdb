from django.contrib import admin
from models import Facility, Fee, Payment, Program
from django.db.models import Sum
from helpers.admin_filters import SelectFilter, BooleanSelectFilter, M2MSelectFilter

class FacilityAdmin(admin.ModelAdmin):
  list_display = ('facility_name', 'doctor_ic', 'full_contact', 'address', 'region', \
                  'district', 'zone', 'programs_list', 'membership', 'edit_balance')
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

  def edit_balance(self, obj):
    id = obj.id
    balance = obj.getBalance(obj.id)
    if balance == 0:
        return '<a class="paid balance" data-id="{0}" href="#">Paid</a>'.format(id)
    return '<a class="balance" data-id="{0}" href="#">{1}</a>'.format(id, balance)
  edit_balance.allow_tags = True


  class Media:
    css = {
      'all': ('css/chosen.css',)
    }
    js = ('scripts/jquery-1.8.3.min.js',
          'scripts/chosen.jquery.min.js')

class FeeAdmin(admin.ModelAdmin):
  list_display = ('type', 'year', 'amount')
  search_fields = ('type', 'year', 'amount')

  filter_horizontal = ('facility',)

  # when saving a fee from admin interface update Facility static fee dict
  def save_related(self, request, form, formsets, change):
    super(FeeAdmin,self).save_related(request, form, formsets, change)
    Facility.updateBalance()

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
  search_fields = ('facility',)

class ProgramAdmin(admin.ModelAdmin):
  list_display = ('name', 'description')

admin.site.register(Facility, FacilityAdmin)
admin.site.register(Fee, FeeAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Program)
