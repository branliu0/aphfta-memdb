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
    return HttpResponse(request.POST.get('facility_name') + 'testing')

def update(request, id=None):
  if request.method == "GET":
    facility = Facility.objects.get(pk=1)
    form = FacilityForm(facility)

    return render(request, 'memdb/register.html',
            {
            })
  elif request.method == 'POST':
