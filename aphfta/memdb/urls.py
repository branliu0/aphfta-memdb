from django.conf.urls import patterns, url

from memdb import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^register$', views.register, name='register'),
    url(r'^update/(?P<id>\d+)$', views.update, name='update'),
    url(r'^payments/(?P<id>\d+)$', views.payment, name='payment'),
    url(r'^payments/(?P<id>\d+)/add$', views.add_payment, name='add-payment'),
)

