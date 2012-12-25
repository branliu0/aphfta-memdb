from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'memdb.views.home', name='home'),
    # url(r'^aphfta/', include('aphfta.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^members/', include('memdb.urls', namespace="memdb")),
    url(r'^admin/', include(admin.site.urls)),
)
