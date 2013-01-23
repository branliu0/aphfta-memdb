from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, render_to_response
from django.template import Context, loader
from django.core.urlresolvers import reverse

from memdb.models import Facility
from memdb.models import Payment
from memdb.models import Fee
from memdb.forms import FacilityForm
from django.db.models import Sum
import datetime
import json

from django.utils import timezone

def index(request):
  return render(request, 'memdb/index.html')

def home(request):
  return render(request, 'memdb/home.html')

def register(request):
  context = {}

  if request.method == "GET":
    facility_name_pos = 0
    outpatient_pos = 10
    lab_pos = 18
    physicians_pos = 27
    average_pos = 48
    submitText = "Register"

    form = list(FacilityForm())
    context.update(locals())
    return render(request, 'memdb/clinicForm.html', context)

  elif request.method == 'POST':
    form = FacilityForm(request.POST)
    if form.is_valid():
        facility = form.save(commit = False)
        facility.date_joined = timezone.now()
        facility.save()
        return HttpResponseRedirect('/')

def update(request, id=None):
  facility = get_object_or_404(Facility, id=id)

  if request.method == "POST":
    form = FacilityForm(request.POST, instance=facility)
    if form.is_valid():
      form.save()
      return HttpResponseRedirect('/')

  elif request.method == "GET":
    form = FacilityForm(instance=facility)

  context = Context({'title': "Update User", 'submitText': "Update", 'form': form})
  return render(request, 'memdb/clinicForm.html', context)

def payment(request, id=None):
    interval = int(request.GET.get("interval", 1))

    range_start = 3 * interval
    range_end = 3 * (interval - 1)

    facility = get_object_or_404(Facility, id=id)
    # error checking
    name = facility.facility_name
    region = facility.region

    now = datetime.datetime.now()
    start_year = now.year - range_start + 1
    end_year = now.year - range_end

    years = {}
    for year in range(start_year, end_year+1):
        years[str(year)] = {'annual_fee': 0, 'paid': 0, 'payments': [] }

    past_years = {}

    recent_fees = Fee.objects.filter(facility=id, year__range=(start_year,end_year))
    old_fees  = Fee.objects.filter(facility=id, year__lt=str(start_year))

    recent_payments = Payment.objects.filter(facility_id=id, date__range=[str(start_year)+"-01-01", str(end_year)+"-12-31"]) \
                              .order_by('date')
    old_payments = Payment.objects.filter(facility_id=id, date__lt=str(start_year)+"-01-01") \
                              .values('amount')

    old_fees_total = sum(map(lambda x: x.amount, old_fees))
    recent_fees_total = sum(map(lambda x: x.amount, recent_fees))

    old_payment_total = sum(map(lambda x: x['amount'], old_payments))
    recent_payment_total = sum(map(lambda x: x.amount, recent_payments))

    past_years["total_fees"] = old_fees_total
    past_years["total_paid"] = old_payment_total
    past_years["balance_remaining"] = old_fees_total - old_payment_total

    for payment in recent_payments:
        year = str(payment.date.year)
        years[year]['payments'].append({"date": payment.date, "amount": payment.amount})
        years[year]['paid'] += payment.amount

    for fee in recent_fees:
        year = str(fee.year)
        years[year]['annual_fee'] += fee.amount

    recent_payments = Payment.objects.filter(facility_id=id, date__range=[str(start_year)+"-01-01", str(end_year)+"-12-31"]) \
                              .order_by('date')

    total_fees = Fee.objects.filter(facility=id, year__lte=now.year).aggregate(Sum('amount'))
    total_payments = Payment.objects.filter(facility_id=id, date__lte=str(now.year)+"-12-31").aggregate(Sum('amount'))
    if not total_fees["amount__sum"]:
      total_fees["amount__sum"] = 0
    if not total_payments["amount__sum"]:
      total_payments["amount__sum"] = 0

    balance = total_fees["amount__sum"] - total_payments["amount__sum"]

    context = Context({"facility_name": name, "balance": balance, "region": region, "years": years, \
                       "past_years": past_years, "facility_id": id, "interval": interval})

    return render(request, 'memdb/payment.html', context)

def add_payment(request, facility_id=None):
    '''
      Handles POST request from payment modal to create new payments.
    '''

    if not request.POST['date']:
        return HttpResponse("error: missing date")
    if not request.POST['amount']:
        return HttpResponse("error: missing amount")

    args = request.POST.dict()

    if len(args) != 2:
        return HttpResponse("error: need only date and amount")

    args['facility_id'] = facility_id

    new_payment = Payment(**args)
    new_payment.save();
    return HttpResponse("success")

def region(request, region=''):
    '''
      When creating a new fee, the user may want to apply the fee to all
      facilities in a region. This function returns just that.
    '''

    # return set of all facilities in region, and compliment of set
    include_facilities = Facility.objects.filter(region=region)
    exclude_facilities = Facility.objects.exclude(region=region)

    include_facility_names = map(lambda x: { 'id': x.id, 'name': x.facility_name }, include_facilities)
    exclude_facility_names = map(lambda x: { 'id': x.id, 'name': x.facility_name }, exclude_facilities)

    all_facilities = {'include': include_facility_names, 'exclude': exclude_facility_names}
    return HttpResponse(json.dumps(all_facilities))
