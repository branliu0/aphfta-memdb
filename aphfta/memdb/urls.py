from django.conf.urls import patterns, url

from memdb import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^register$', views.register, name='register'),
    url(r'^update/(?P<id>\d+)$', views.update, name='update'),
)

