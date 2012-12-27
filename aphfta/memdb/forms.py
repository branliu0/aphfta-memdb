from django.forms import ModelForm
from memdb.models import Facility

class FacilityForm(ModelForm):
  class Meta:
    model = Facility
    exclude = ('date_joined', 'hospital_health_maternity', 'tel_office2', 'tel_office3', 'email2', 'email3', 'district', 'region', 'membership', 'membership_type')

'''
class OtherStaffForm(ModelForm):
  class Meta:
    model = OtherStaff

class WardForm(ModelForm):
  class Meta:
    model = Ward
'''
