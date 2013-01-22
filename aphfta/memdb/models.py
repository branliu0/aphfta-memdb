from django.db import models
from helpers import model_helpers
from django.db.models import Sum

# Create your models here.
class Facility(models.Model):
  facility_name = models.CharField('Facility Name', max_length=200)
  date_joined = models.DateField(auto_now_add=True, null=True)
  address = models.CharField('Address', max_length=250, blank=True)
  district = models.CharField('District', max_length=250, blank=True)
  region = models.CharField('Region', max_length=250, blank=True)
  tel_office = models.CharField('Tel No. Office', max_length=250, blank=True)
  tel_office2 = models.CharField('Tel No. Office 2', max_length=250, blank=True)
  tel_office3 = models.CharField('Tel No. Office 3', max_length=250, blank=True)
  tel_mobile = models.CharField('Tel No. Mobile', max_length=250, blank=True)
  fax = models.CharField('Fax', max_length=250, blank=True)
  email = models.EmailField('Email', blank=True)
  email2 = models.EmailField('Email 2', blank=True)
  email3 = models.EmailField('Email 3', blank=True)
  moh_reg_cert = models.IntegerField('MOH Facility Registration Certificate No.', blank=True, null=True)
  FACILITY_TYPE = (
         ("VO", 'Vountary Agency'),
         ("PR", 'Private'),
         ("CH", 'Charitable Organisation')
  )
  facility_type = models.CharField('Facility Type', max_length=2,
                                   choices=FACILITY_TYPE, blank=True)
  membership = models.NullBooleanField("APHFTA Member")
  membership_type = models.CharField("Membership Type", max_length=250, blank=True)

  doctor_ic = models.CharField('Doctor In Charge', max_length=250, blank=True)
  qualifications = models.CharField('Qualifications', max_length=500, blank=True)
  outpatient = models.CharField('Outpatient', max_length=500, blank=True)
  inpatient = models.CharField('Inpatient', max_length=500, blank=True)
  wards = models.TextField(blank=True)

  hospital_health_maternity = models.NullBooleanField('Hospital, Health Centre, Dispensary, Maternity Homes', blank=True, null=True)

  major_operation_theaters = models.IntegerField('Major Operation Theatres', blank=True, null=True)
  minor_operation_theaters = models.IntegerField('Minor Operation Theatres', blank=True, null=True)
  delivery_beds = models.IntegerField('Delivery Beds', blank=True, null=True)

  antenatal_mch_serices = models.CharField('Antenatal / MCH Services', max_length=500, blank=True)
  other_speciality_services = models.CharField('Other Facility/Speciality Services', max_length=500, blank=True)

  lab = models.NullBooleanField('Laboratory')
  xray = models.NullBooleanField('X-Ray Services')
  blood_bank = models.NullBooleanField('Blood Bank')
  pharmacy = models.NullBooleanField('Pharmacy')
  dental = models.NullBooleanField('Dental Services')
  ultrasonography = models.NullBooleanField('Ultrasonography')
  physiotherapy = models.NullBooleanField('Physiotherapy')
  icu = models.NullBooleanField('ICU')
  ambulance = models.NullBooleanField('Ambulance Services')

  physicians = models.IntegerField('Physicians', blank=True, null=True)
  surgeons = models.IntegerField('Surgeons', blank=True, null=True)
  obstetricians = models.IntegerField('Obstetricians', blank=True, null=True)
  paediatricians = models.IntegerField('Paediatricians', blank=True, null=True)

  medical_officers = models.IntegerField('Medical Officers', blank=True, null=True)
  assistant_medical_officers = models.IntegerField('Assistant Medical Officers', blank=True, null=True)
  clinical_officers = models.IntegerField('Assistant Medical Officers', blank=True, null=True)
  assistant_clinical_officers = models.IntegerField('Clinical Officers', blank=True, null=True)
  dental_officers = models.IntegerField('Dental Officers', blank=True, null=True)
  dental_assistants = models.IntegerField('Dental Assistants', blank=True, null=True)

  nurses_grade_A = models.IntegerField('Nurses Grade A', blank=True, null=True)
  nurses_grade_B = models.IntegerField('Nurses Grade B', blank=True, null=True)
  nursing_assistants = models.IntegerField('Nursing Assistants', blank=True, null=True)
  ward_attendants = models.IntegerField('Ward Attendants', blank=True, null=True)

  lab_technologists = models.IntegerField('Lab Technologists', blank=True, null=True)
  lab_technicians = models.IntegerField('Lab Technicians', blank=True, null=True)
  lab_assistants = models.IntegerField('Lab Assistants', blank=True, null=True)

  rad_technologists = models.IntegerField('Radiographic Technologists', blank=True, null=True)
  rad_technicians = models.IntegerField('Radiographic Technicians', blank=True, null=True)
  rad_assistants = models.IntegerField('Radiographic Assistants', blank=True, null=True)
  other_staff = models.TextField(blank=True)

  avg_outpatients_daily = models.IntegerField('Average Outpatients Seen /Day', blank=True, null=True)
  avg_inpatients_daily = models.IntegerField('Average Inpatients Seen /Day', blank=True, null=True)
  avg_deliveries_month = models.IntegerField('Average Deliveries /Month', blank=True, null=True)
  avg_mch_attendance_month = models.IntegerField('Average MCH Attendance /Month', blank=True, null=True)

  def full_contact(self):
    contacts = [
      "(o) " + self.tel_office,
      "(o) " + self.tel_office2,
      "(o) " + self.tel_office3,
      "(m) " + self.tel_mobile,
      "(f) " + self.fax,
      "(e) " + self.email,
      "(e) " + self.email2,
      "(e) " + self.email3
    ]
    return "<br />".join([c for c in contacts if len(c) > 4])
  full_contact.short_description = "Contact"
  full_contact.allow_tags = True

  def balance(self):
    fees = Fee.objects.filter(facility=self.id).aggregate(Sum('amount'))
    print fees
    payments = Payment.objects.filter(facility=self.id).aggregate(Sum('amount'))
    print payments

    if fees['amount__sum'] == None:
      fees['amount__sum'] = 0
    if payments['amount__sum'] == None:
      payments['amount__sum'] = 0

    return fees['amount__sum'] - payments['amount__sum']

  def __unicode__(self):
    return self.facility_name

  class Meta:
    app_label = model_helpers.string_with_title("memdb", "Facility Information")
    verbose_name_plural = 'facilities'

class Payment(models.Model):
  facility = models.ForeignKey(Facility)
  date = models.DateField()
  amount = models.IntegerField()

  def __unicode__(self):
    return str(self.facility) + ': ' + str(self.amount)

class Fee(models.Model):
  type = models.CharField('Fee Type', max_length=250)
  year = models.IntegerField()
  description = models.TextField(blank=True)
  amount = amount = models.IntegerField()
  facility = models.ManyToManyField(Facility)

  def __unicode__(self):
    return "%s %d" % (self.type, self.year)
