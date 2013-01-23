from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import User, Group
from models import Facility, Program
from helpers.admin_filters import SelectFilter, BooleanSelectFilter, M2MSelectFilter


class FacilityAdmin(admin.ModelAdmin):
  list_display = ('facility_name', 'doctor_ic', 'full_contact', 'address', 'region', 'district', 'zone', 'programs_list', 'completeness', 'membership')
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

  # Manually override the queryset function so as to prefetch related programs, so that
  # the `programs_list` method doesn't result in an additional query.
  def queryset(self, request):
    qs = super(FacilityAdmin, self).queryset(request)
    return qs.prefetch_related('programs')

  class Media:
    css = {
      'all': ('css/chosen.css',)
    }
    js = ('scripts/jquery-1.8.3.min.js',
          'scripts/chosen.jquery.min.js')


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
admin.site.register(Program, ProgramAdmin)
admin.site.unregister(Group)
admin.site.register(Group, MyGroupAdmin)
