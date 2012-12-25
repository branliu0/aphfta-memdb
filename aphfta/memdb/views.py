from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, render_to_response
from django.template import Context, loader
from django.core.urlresolvers import reverse

from memdb.models import Facility, OtherStaff, Ward
from memdb.models import FacilityForm, OtherStaffForm, WardForm

def index(request):
  return render(request, 'memdb/index.html')

def home(request):
  return render(request, 'memdb/home.html')

def register(request):
  context = {}

  if request.method == "GET":
    facility_name_pos = 0
    outpatient_pos = 10
    lab_pos = 17
    physicians_pos = 26
    average_pos = 46

    form = list(FacilityForm())
    context.update(locals())
    return render(request, 'memdb/register.html', context)

  elif request.method == 'POST':
    form = FacilityForm(request.POST)
    if form.is_valid():
        form.save()
        return http.HttpResponseRedirect('/')

def update(request, id=None):
  facility = get_object_or_404(Facility, id=id)

  if request.method == "POST":
    form = FacilityForm(request.POST, instance=facility)
    if form.is_valid():
      form.save()
      return http.HttpResponseRedirect('/')

  elif request.method == "GET":
    form = FacilityForm(instance = facility)

  context = Context({'title': "Update User", 'form': form})
  return render(request, 'memdb/register.html', context)
