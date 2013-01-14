from django.conf.urls import patterns, include, url

import report_builder

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # url(r'^$', 'memdb.views.home', name='home'),

    # url(r'^members/', include('memdb.urls', namespace="memdb")),
    # url(r'^admin/', include(admin.site.urls)),
    url(r'', include(admin.site.urls)),
    url(r'^report_builder/', include('report_builder.urls')),
)
