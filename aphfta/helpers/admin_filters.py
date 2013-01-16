from django.contrib import admin
from django.template.defaultfilters import slugify, title
from django.utils.encoding import force_unicode

# A base class that defines some shared functionality.
# In particular, it sets the template, and properly sets the title to the
# verbose_name of the field.
class SelectFilterBase(admin.SimpleListFilter):
  template = "admin/select_filter.html"

  def __init__(self, request, params, model, model_admin):
    try:
      field = next(x for x in model._meta.fields if x.name == self.field_name)
      self.title = title(getattr(field, 'verbose_name', self.field_name))
    except StopIteration:
      # This will happen if the field couldn't be found. This happens for
      # `ManyToManyField`s because they are treated differently from other fields.
      # If the verbose_name is needed, we can also search through
      # `model._meta.local_many_to_many`, but it's not needed at the moment
      self.title = self.field_name
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
        kwargs = {
          self.field_name: self.value()
        }
        return qs.filter(**kwargs)
      else:
        return qs

    def lookups(self, request, model_admin):
      lookups = []
      for v in model_admin.model.objects.values_list(self.field_name).distinct():
        value = str(v[0])
        if value:
          # We need to truncate the values so that the select box doesn't
          # get too long and overflow out of the DIV
          # Also, Django 1.3 doesn't have the truncatechars filter, so
          # I'm rewriting it here...
          truncated = value if len(value) <= 18 else value[0:14] + "..."
          lookups.append((value, truncated))
      return sorted(lookups)

  return SelectFilter

# Quite similar to the above select filter, except this is for boolean values.
def makeBooleanSelectFilter(field):
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

def makeMultiselectFilter(field):
  SelectFilter = makeSelectFilter(field)

  class MultiselectFilter(SelectFilter):
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
