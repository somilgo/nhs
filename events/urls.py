from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
	url(r'^$', views.home, name='home'),
	url(r'^sign_up/$', views.sign_up, name='sign_up'),
	url(r'^sign_up_success/$', views.sign_up_success, name='sign_up_success'),
	url(r'^log_in/$', views.log_in, name='log_in'),
	url(r'^log_in_success/$', views.log_in_success, name='log_in_success'),
	url(r'^event_creator/$', views.event_creator, name='event_creator'),
	url(r'^event_success/$', views.event_success, name='event_success'),
	url(r'^(?P<pk>[0-9]+)/$', views.event_details, name = 'event-detail'),
	url(r'^(?P<year>[0-9]+)/(?P<month>[0-9]+)/$', views.calendar, name='calendarView'),
	url(r'^(?P<event_pk>[0-9]+)/event_sign_up/$', views.event_sign_up, name='event_sign_up'),
	url(r'^(?P<pk>[0-9]+)/event_unsign_up/$', views.un_sign, name='un_sign'),
]