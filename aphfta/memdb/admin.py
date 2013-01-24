from django import forms
from django.contrib import admin
from models import Facility, Fee, Payment, Program
from django.db.models import Sum
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import User, Group
from helpers.admin_filters import SelectFilter, FKSelectFilter, BooleanSelectFilter, M2MSelectFilter

class FacilityAdmin(admin.ModelAdmin):
  list_display = ('facility_name', 'doctor_ic', 'full_contact', 'address', 'region', \
                  'district', 'zone', 'programs_list', 'completeness')

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

  # This puts the bar of save buttons at the top of the admin edit page as well
  save_on_top = True

  def edit_balance(self, obj):
    '''
      Displays link on balance column for editting facility payments
    '''
    balance = obj.balance()
    # green balance button with + symbol if facility pays more than is owed
    if balance < 0:
      return '<a class="balance" style="font-weight:bold;color:green" data-id="{0}" href="#">+{1}</a>'\
          .format(obj.id, "Paid" if balance == 0 else abs(balance))
    return '<a class="balance" data-id="{0}" href="#">{1}</a>'\
        .format(obj.id, "Paid" if balance == 0 else abs(balance))
  edit_balance.short_description = "Edit Balance"
  edit_balance.allow_tags = True

  # Manually override the queryset function so as to prefetch related programs, so that
  # the `programs_list` method doesn't result in an additional query.
  def queryset(self, request):
    qs = super(FacilityAdmin, self).queryset(request)
    return qs.prefetch_related('programs', 'fees', 'payments')

  # Dynamically modify the changelist class so that the balance column is only
  # shown if the user has permissions to add or edit payments.
  def get_changelist(self, request):
    BaseChangeList = super(FacilityAdmin, self).get_changelist(request)
    class ChangeList(BaseChangeList):
      def __init__(self, *args, **kwargs):
        super(ChangeList, self).__init__(*args, **kwargs)
        if request.user.has_perm('memdb.add_payment') or\
            request.user.has_perm('memdb.edit_payment'):
          self.list_display += ('edit_balance',)
    return ChangeList

  class Media:
    css = {
      'all': ('css/chosen.css',
              'css/jquery-ui-1.9.2.custom.min.css',
              'css/admin-facility.css',
              'css/payments.css',
             )
    }
    js = ('scripts/jquery-1.8.3.min.js',
          'scripts/chosen.jquery.min.js',
          'scripts/jquery-ui-1.9.2.custom.min.js',
          'scripts/jquery.simplemodal-1.4.3.js',
          )

class FeeAdmin(admin.ModelAdmin):
  list_display = ('type', 'year', 'amount')
  search_fields = ('type', 'year', 'amount', 'facility__facility_name')

  list_filter = (
    M2MSelectFilter('facility', 'facility_name'),
  )

  filter_horizontal = ('facility',)

  class Media:
    css = {
      'all': ('css/chosen.css',)
    }

    js = ('scripts/jquery-1.8.3.min.js',
          'scripts/chosen.jquery.min.js',
         )

  # when saving a fee from admin interface update Facility static fee dict

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

  list_filter = (
    FKSelectFilter('facility', 'facility_name'),
  )

  class Media:
    css = {
      'all': ('css/chosen.css',)
    }

    js = ('scripts/jquery-1.8.3.min.js',
          'scripts/chosen.jquery.min.js',
         )



class ProgramAdminForm(forms.ModelForm):
  facilities = forms.ModelMultipleChoiceField(
      queryset=Facility.objects.all(),
      required=False,
      widget=FilteredSelectMultiple(
          verbose_name='Facilities',
          is_stacked=False))

  def __init__(self, *args, **kwargs):
    super(ProgramAdminForm, self).__init__(*args, **kwargs)

    if self.instance and self.instance.pk:
      self.fields['facilities'].initial = self.instance.facilities.all()

  def save(self, commit=True):
    program = super(ProgramAdminForm, self).save(commit=False)

    if commit:
      program.save()

    if program.pk:
      program.facilities = self.cleaned_data['facilities']
      self.save_m2m()

    return program

  class Meta:
    model = Program

class ProgramAdmin(admin.ModelAdmin):
  list_display = ('name', 'description')
  form = ProgramAdminForm

class GroupAdminForm(forms.ModelForm):
  users = forms.ModelMultipleChoiceField(
      queryset=User.objects.all(),
      required=False,
      widget=FilteredSelectMultiple(
          verbose_name='Users',
          is_stacked=False))

  def __init__(self, *args, **kwargs):
    super(GroupAdminForm, self).__init__(*args, **kwargs)

    if self.instance and self.instance.pk:
      self.fields['users'].initial = self.instance.user_set.all()

  def save(self, commit=True):
    group = super(GroupAdminForm, self).save(commit=False)

    if commit:
      group.save()

    if group.pk:
      group.user_set = self.cleaned_data['users']
      self.save_m2m()

    return group

  class Meta:
    model = Group

class MyGroupAdmin(GroupAdmin):
  form = GroupAdminForm

admin.site.register(Facility, FacilityAdmin)
admin.site.register(Fee, FeeAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Program, ProgramAdmin)
admin.site.unregister(Group)
admin.site.register(Group, MyGroupAdmin)
