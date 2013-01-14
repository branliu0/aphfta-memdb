from django.contrib import admin
from django.template.defaultfilters import slugify, truncatechars
from models import Facility

# A base class that defines some shared functionality.
# In particular, it sets the template, and properly sets the title to the
# verbose_name of the field.
class SelectFilterBase(admin.SimpleListFilter):
    template = "admin/select_filter.html"

    def __init__(self, request, params, model, model_admin):
        self.field = next(x for x in model._meta.fields if x.name == self.field_name)
        self.title = getattr(self.field, 'verbose_name', self.field_name)
        self.parameter_name = self.field_name
        super(SelectFilterBase, self).__init__(request, params, model, model_admin)

# Generates a SelectFilter class for the given field. Nearly identical to the
# default Django filter, except that it uses a HTML select rather than an
# unordered list.
def makeSelectFilter(field):
    class SelectFilter(SelectFilterBase):
        field_name = field

        def queryset(self, request, qs):
            if self.value():
                kwargs = {}
                kwargs[self.field_name] = self.value()
                return qs.filter(**kwargs)
            else:
                return qs

        def lookups(self, request, model_admin):
            lookups = []
            for d in model_admin.model.objects.values(self.field_name).distinct():
                value = d[self.field_name]
                if value:
                    # We need to truncate the values so that the select box doesn't
                    # get too long and overflow out of the DIV
                    lookups.append((value, truncatechars(value, 18)))
            return sorted(lookups)
    return SelectFilter

# Quite similar to the above select filter, except this is for boolean values.
def makeBooleanSelectFilter(field):
    class SelectFilter(SelectFilterBase):
        field_name = field

        def queryset(self, request, qs):
            if self.value():
                kwargs = {}
                kwargs[self.field_name + "__exact"] = self.value()
                return qs.filter(**kwargs)
            else:
                return qs

        def lookups(self, request, model_admin):
            return [
                (0, "No"),
                (1, "Yes"),
            ]
    return SelectFilter

class FacilityAdmin(admin.ModelAdmin):
  list_display = ('facility_name', 'doctor_ic', 'tel_office', 'email', 'region', 'district', 'membership_type', 'membership')
  search_fields = ('facility_name', 'doctor_ic', 'tel_office', 'moh_reg_cert', 'email')
  list_filter = (
      makeSelectFilter('membership_type'),
      makeSelectFilter('region'),
      makeSelectFilter('district'),
      makeBooleanSelectFilter('lab'),
      makeBooleanSelectFilter('xray'),
      makeBooleanSelectFilter('blood_bank'),
      makeBooleanSelectFilter('pharmacy'),
      makeBooleanSelectFilter('dental'),
      makeBooleanSelectFilter('ultrasonography'),
      makeBooleanSelectFilter('icu'),
      makeBooleanSelectFilter('ambulance'),
  )
  ordering = ('facility_name',)

admin.site.register(Facility, FacilityAdmin)
