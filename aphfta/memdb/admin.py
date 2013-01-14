from django.contrib import admin
from django.template.defaultfilters import slugify, truncatechars
from models import Facility

def makeSelectFilter(field):
    class SelectFilter(admin.SimpleListFilter):
        template = "admin/select_filter.html"
        title = field
        parameter_name = field

        def queryset(self, request, qs):
            if self.value():
                kwargs = {}
                kwargs[field] = self.value()
                return qs.filter(**kwargs)
            else:
                return qs

        def lookups(self, request, model_admin):
            lookups = []
            for d in model_admin.model.objects.values(field).distinct():
                value = d[field]
                if value:
                    # We need to truncate the values so that the select box doesn't
                    # get too long and overflow out of the DIV
                    lookups.append((value, truncatechars(value, 18)))
            return sorted(lookups)
    return SelectFilter

class FacilityAdmin(admin.ModelAdmin):
  list_display = ('facility_name', 'doctor_ic', 'tel_office', 'email', 'region', 'district', 'membership_type', 'membership')
  search_fields = ('facility_name', 'doctor_ic', 'tel_office', 'moh_reg_cert', 'email')
  list_filter = (
      makeSelectFilter('membership_type'),
      makeSelectFilter('region'),
      makeSelectFilter('district'),
  )
  ordering = ('facility_name',)

admin.site.register(Facility, FacilityAdmin)
