from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, render_to_response
from django.template import Context, loader
from django.core.urlresolvers import reverse

from memdb.models import Facility
from memdb.models import Payment
from memdb.forms import FacilityForm
import datetime

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
    history_range = 4

    facility = get_object_or_404(Facility, id=id)
    name = facility.facility_name
    balance = facility.balance
    email = facility.email

    now = datetime.datetime.now()
    past_year = now.year - history_range + 1;

    years = {}
    for year in range(past_year, now.year+1):
        years[str(year)] = {'annual_fee': 2000, 'paid': 100, 'payments': [] }

    payments = Payment.objects.filter(facility_id=id, date__range=[str(past_year)+"-01-01", now.strftime("%Y-%m-%d")]) \
                              .order_by('date')

    for payment in payments:
        years[str(payment.date.year)]['payments'].append({"date": payment.date, "amount": payment.amount})

    print years
    context = Context({'facility': name, "balance": balance, "zone": email, "years": years})
    return render(request, 'memdb/payment.html', context)

def add_payment(request, id=None):
    print request.POST
    return HttpResponse("hi")
