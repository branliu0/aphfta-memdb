from operator import itemgetter

from django.contrib import admin
from django.core.exceptions import FieldError
from django.template.defaultfilters import slugify, title
from django.utils.encoding import force_unicode

# A base class that defines some shared functionality.
# In particular, it sets the template, and properly sets the title to the
# verbose_name of the field.
class SelectFilterBase(admin.SimpleListFilter):
  template = "admin/select_filter.html"

  def __init__(self, request, params, model, model_admin):
    if not self.title:
      try:
        self.field = next(x for x in model._meta.fields if x.name == self.field_name)
        self.title = title(getattr(self.field, 'verbose_name', self.field_name))
      except StopIteration:
        raise FieldError("The field %s could not be found on the model %s" %
                        (self.field_name, model.__name__))
    self.parameter_name = self.field_name
    super(SelectFilterBase, self).__init__(request, params, model, model_admin)

# Generates a SelectFilter class for the given field. Nearly identical to the
# default Django filter, except that it uses a HTML select rather than an
# unordered list.
def SelectFilter(field):
  class SelectFilter(SelectFilterBase):
    field_name = field

    def queryset(self, request, qs):
      if self.value():
        kwargs = {
          self.field_name: self.value()
        }
        return qs.filter(**kwargs)
      else:
        return qs

    def lookups(self, request, model_admin):
      lookups = []
      for v in model_admin.model.objects.values_list(self.field_name).distinct():
        key = value = str(v[0])

        # If the field we're dealing with has an enum, then show the value of the enum
        # rather than the enum key
        if self.field and self.field._choices:
          try:
            choice = next(v for v in self.field._choices if v[0] == value)
            value = choice[1]
          except StopIteration:
            pass
        if value:
          lookups.append((key, value))
      return sorted(lookups)

  return SelectFilter

# Quite similar to the above select filter, except this is for boolean values.
def BooleanSelectFilter(field):
  class SelectFilter(SelectFilterBase):
    field_name = field

    def queryset(self, request, qs):
      if self.value():
        kwargs = {
          self.field_name + "__exact": self.value()
        }
        return qs.filter(**kwargs)
      else:
        return qs

    def lookups(self, request, model_admin):
      return [
        (0, "No"),
        (1, "Yes"),
      ]

  return SelectFilter

def MultiselectFilter(field):
  SelectFilterClass = SelectFilter(field)

  class MultiselectFilter(SelectFilterClass):
    template = "admin/multiselect_filter.html"

    def queryset(self, request, qs):
      if self.value():
        kwargs = {
          self.field_name + "__in": self.value().split(",")
        }
        return qs.filter(**kwargs)
      else:
        return qs

    # Extending the choices method for multiselect functionality
    # 1. Remove the "All" choice
    # 2. Include the choice value in the context, so that the corresponding
    # javascript can properly generate the URL parameter
    # 3. Include a base_query_string parameter, which includes all the other URL
    # parameters. Also necessary for properly generating the URL parameter.
    # 4. Properly checking for selection of the choice
    def choices(self, cl):
      for lookup, title in self.lookup_choices:
        yield {
          'base_query_string': cl.get_query_string({}, [self.parameter_name]),
          'selected': self.value() is not None and force_unicode(lookup) in self.value().split(","),
          'query_string': cl.get_query_string({ self.parameter_name: lookup }, []),
          'display': title,
          'value': lookup,
        }

  return MultiselectFilter

def M2MSelectFilter(field, foreign_display_field):
  SelectFilterClass = SelectFilter(field)

  class M2MSelectFilter(SelectFilterClass):

    def __init__(self, request, params, model, model_admin):
      try:
        self.field = next(f for f in model._meta.local_many_to_many
                          if f.name == field)
        self.title = title(getattr(self.field, 'verbose_name', self.field_name))
      except StopIteration:
        raise FieldError("ManyToManyField %s could not be found on the model %s" %
                         (field_name, model.__name__))
      super(M2MSelectFilter, self).__init__(request, params, model, model_admin)

    def lookups(self, request, model_admin):
      lookups = super(M2MSelectFilter, self).lookups(request, model_admin)
      new_lookups = []
      related_model = self.field.related.parent_model
      foreign_lookup = related_model.objects.values('id', foreign_display_field)
      for lookup, title in lookups:
        try:
          id = int(lookup)
          title = next(f for f in foreign_lookup if f["id"] == int(lookup))[foreign_display_field]
        except ValueError, StopIteration:
          # Only let actual field values be valid choices
          continue
        new_lookups.append((lookup, title))
      return sorted(new_lookups, key=itemgetter(1))

  return M2MSelectFilter
