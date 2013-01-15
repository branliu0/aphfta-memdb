from django.contrib import admin
from django import forms
from django.core.urlresolvers import reverse
from report_builder.models import DisplayField, Report, FilterField


class DisplayFieldForm(forms.ModelForm):
    position = forms.IntegerField(widget=forms.HiddenInput, required=False)
    class Meta:
        model = DisplayField

class DisplayFieldInline(admin.StackedInline):
    model = DisplayField
    form = DisplayFieldForm
    extra = 0
    sortable_field_name = "position"

class FilterFieldForm(forms.ModelForm):
    position = forms.IntegerField(widget=forms.HiddenInput)
    class Meta:
        model = FilterField

class FilterFieldInline(admin.StackedInline):
    model = FilterField
    form = FilterFieldForm
    extra = 0
    sortable_field_name = "position"
    
class ReportAdmin(admin.ModelAdmin):
    list_display = ('edit_report', 'name', 'download_excel_spreadsheet', 'created', 'modified')
    inlines = [DisplayFieldInline, FilterFieldInline]
    list_display_links = []
    
    def edit_report(self, obj):
        return '<a href="%s">Edit</a>' % obj.get_absolute_url()
    edit_report.allow_tags = True
    def admin_edit(self, obj):
        return 'Admin Edit'
    def download_excel_spreadsheet(self, obj):
        return '<a href="%s">Download</a>' % reverse('report_builder.views.download_xlsx', args=[obj.id])
    download_excel_spreadsheet.allow_tags = True

admin.site.register(Report, ReportAdmin)
