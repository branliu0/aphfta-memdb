from django.conf.urls import patterns, url

from memdb import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^payments/(?P<id>\d+)$', views.payment, name='payment'),
    url(r'^payments/(?P<facility_id>\d+)/add$', views.add_payment, name='add-payment'),
    url(r'^regions/(?P<region>[a-zA-Z]+)$', views.region, name='region'),
)

