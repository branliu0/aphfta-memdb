from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, render_to_response
from django.template import Context, loader
from django.core.urlresolvers import reverse

from memdb.models import Facility, OtherStaff, Ward
from memdb.models import FacilityForm, OtherStaffForm, WardForm

def index(request):
    return render(request, 'memdb/index.html')

def register(request):

    if request.method == "GET":
      facility_name_pos = 0
      outpatient_pos = 10
      lab_pos = 17
      physicians_pos = 26
      average_pos = 46

      form = list(FacilityForm())

      section1 = form[facility_name_pos:outpatient_pos]
      section2 = form[outpatient_pos:lab_pos]
      section3 = form[lab_pos:physicians_pos]
      section4 = form[physicians_pos:average_pos]
      section5 = form[average_pos:]

      return render(request, 'memdb/register.html',
              {'section1': section1,
               'section2': section2,
               'section3': section3,
               'section4': section4,
               'section5': section5
              })
    elif request.method == 'POST':
      return HttpResponse(request.POST.get('facility_name') + 'testing')
