from django.db import models
from django.forms import ModelForm

# Create your models here.
class Facility(models.Model):
    date_joined = models.DateTimeField('Date Joined')
    facility_name = models.CharField('Facility Name', max_length=200)
    address = models.CharField('Address', max_length=250)
    tel_office = models.CharField('Tel No. Office', max_length=250)
    tel_mobile = models.CharField('Tell No. Mobile', max_length=250)
    fax = models.CharField('Fax', max_length=250)
    email = models.EmailField('Email')
    moh_reg_cert = models.IntegerField('Ministry of Health Facility Registration Certificate No.')
    FACILITY_TYPE = (
           ("VO", 'Vountary Agency'),
           ("PR", 'Private'),
           ("CH", 'Charitable Organisation')
    )
    facility_type = models.CharField('Facility Type', max_length=2,
                                     choices=FACILITY_TYPE)

    doctor_ic = models.CharField('Doctor In Charge', max_length=250)
    qualifications = models.CharField('Qualifications', max_length=500)
    outpatient = models.CharField('Outpatient', max_length=500)
    inpatient = models.CharField('Impatient', max_length=500)

    hospital_health_maternity = models.BooleanField('Hospital, Health Centre, Dispensary, Maternity Homes')

    major_operation_theaters = models.IntegerField('Major Operation Theatres')
    minor_operation_theaters = models.IntegerField('Minor Operation Theatres')
    delivery_beds = models.IntegerField('Delivery Beds')

    antenatal_mch_serices = models.CharField('Antenatal / MCH Services', max_length=500)
    other_speciality_services = models.CharField('Other Facility/Speciality Services', max_length=500)

    lab = models.BooleanField('Laboratory')
    xray = models.BooleanField('X-Ray Services')
    blood_bank = models.BooleanField('Blood Bank')
    pharmacy = models.BooleanField('Pharmacy')
    dental = models.BooleanField('Dental Services')
    ultrasonography = models.BooleanField('Ultrasonography')
    physiotherapy = models.BooleanField('Physiotherapy')
    icu = models.BooleanField('ICU')
    ambulance = models.BooleanField('Ambulance Services')

    physicians = models.IntegerField('Physicians')
    surgeons = models.IntegerField('Surgeons')
    obstetricians = models.IntegerField('Obstetricians')
    paediatricians = models.IntegerField('Paediatricians')

    medical_officers = models.IntegerField('Medical Officers')
    assistant_medical_officers = models.IntegerField('Assistant Medical Officers')
    clinical_officers = models.IntegerField('Assistant Medical Officers')
    assistant_clinical_officers = models.IntegerField('Clinical Officers')
    dental_officers = models.IntegerField('Dental Officers')
    dental_assistants = models.IntegerField('Dental Assistants')

    nurses_grade_A = models.IntegerField('Nurses Grade A')
    nurses_grade_B = models.IntegerField('Nurses Grade B')
    nursing_assistants = models.IntegerField('Nursing Assistants')
    ward_attendants = models.IntegerField('Ward Attendants')

    lab_technologists = models.IntegerField('Lab Technologists')
    lab_technicians = models.IntegerField('Lab Technicians')
    lab_assistants = models.IntegerField('Lab Assistants')

    rad_technologists = models.IntegerField('Radiographic Technologists')
    rad_technicians = models.IntegerField('Radiographic Technicians')
    rad_assistants = models.IntegerField('Radiographic Assistants')

    avg_outpatients_daily = models.IntegerField('Average Outpatients Seen /Day')
    avg_inpatients_daily = models.IntegerField('Average Inpatients Seen /Day')
    avg_deliveries_month = models.IntegerField('Average Deliveries /Month')
    avg_mch_attendance_month = models.IntegerField('Average MCH Attendance /Month')

    def __unicode__(self):
        return self.facility_name

class OtherStaff(models.Model):
    staff_type = models.CharField(max_length = 250)
    num = models.IntegerField()
    facility = models.ForeignKey(Facility)
    def __unicode__(self):
        return self.staff_type

class Ward(models.Model):
    ward_type = models.CharField(max_length = 200)
    num_beds = models.IntegerField()
    facility = models.ForeignKey(Facility)
    def __unicode__(self):
        return self.ward_type

class FacilityForm(ModelForm):
    class Meta:
        model = Facility
        exclude = ('date_joined', 'hospital_health_maternity',)

class OtherStaffForm(ModelForm):
    class Meta:
        model = OtherStaff

class WardForm(ModelForm):
    class Meta:
        model = Ward
