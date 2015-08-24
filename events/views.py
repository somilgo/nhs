from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .forms import *
from django.core.context_processors import csrf
from django.contrib.auth import login, authenticate
from events.models import *
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from .eventCalendar import EventCalendar
import datetime
from django.template import RequestContext

# Create your views here.

def home(request):
	request.session['post_log'] = '/'
	try:
		student = Student.objects.get(email=request.session['user'])
		logged = True
	except:
		logged = False
		student = None
	return render(request, 'events/home.html', {'foo':'bar'}, context_instance=RequestContext(request))


def sign_up(request):
	request.session['user'] = None
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/sign_up_success/')
	else:
		form = RegistrationForm()

	return render(request, 'events/sign_up.html', {'form': form})

def sign_up_success(request):
	return HttpResponseRedirect('/log_in/')

def log_in(request):
	form = LogIn(request.POST or None)

	if form.is_valid():
		email = form.cleaned_data['email']
		password = form.cleaned_data['password']
		user = authenticate(email=email, password=password)
		if user is not None:
			request.session['user'] = email
			try:
				return HttpResponseRedirect(request.session['post_log'])
			except:
				return HttpResponseRedirect('/')
		else:
			messages.warning(request, "Username or password is incorrect.")
	return render(request, 'events/log_in.html', {'form':form})

def log_in_success(request):
	return HttpResponse("{} has logged in!".format(request.session['user']))

def event_creator(request):
	try:
		student = Student.objects.get(email=request.session['user'])
	except:
		return HttpResponseRedirect('/log_in/')
	if not student.is_officer:
		return HttpResponse("You need to be an officer to see this page")
	if request.method == 'POST':
		form = EventForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/')
	else:
		form = EventForm()

	return render(request, 'events/event_creator.html', {'form': form})

def event_success(request):
	return HttpResponse("Your event has been successfully created!")

class EventDetailView(DetailView):
	model = Event

def event_details(request, pk):
	event = Event.objects.get(pk=pk)
	try:
		student = Student.objects.get(email=request.session['user'])
	except:
		return HttpResponseRedirect('/log_in/')
	signed_up = False
	full = True
	if student in event.current_students.all():
		signed_up = True
	if event.num_students < event.max_students:
		full = False
	month = event.date.month
	year = event.date.year
	return render_to_response('events/event_detail.html', {'object':event, 'full':full, 
		'signed_up':signed_up, 'month':month, 'year':year, 'my':request.session['myev'], 'officer':student.is_officer},
		context_instance=RequestContext(request))

def calendar(request, year, month):
	myYear = int(year)
	myMonth = int(month)
	events = Event.objects.order_by('start_time').filter(
		date__year=myYear, date__month=myMonth)
	try:
		student = Student.objects.get(email=request.session['user'])
	except:
		student = None
	cal = EventCalendar(events, student).formatmonth(myYear,myMonth)
	if myMonth == 12:
		nextMonth = 1
		nextYear = myYear+1
	else:
		nextYear = myYear
		nextMonth = myMonth+1
	nextUrl = '/{0}/{1}/'.format(nextYear, nextMonth)

	if myMonth == 1:
		prevMonth = 12
		prevYear = myYear-1
	else:
		prevYear = myYear
		prevMonth = myMonth-1
	prevUrl = '/{0}/{1}/'.format(prevYear, prevMonth)
	request.session['myev'] = False
	return render_to_response('events/calendar.html', {'calendar':mark_safe(cal), 'next':nextUrl, 'prev':prevUrl})

def event_sign_up(request, event_pk):
	event = Event.objects.get(pk=event_pk)
	try:
		student = Student.objects.get(email=request.session['user'])
	except:
		return HttpResponseRedirect('/log_in/')
	if event.num_students < event.max_students:
		if student not in event.current_students.all():
			event.current_students.add(student)
			event.save()
			return HttpResponseRedirect("/{}/".format(event_pk))
		return HttpResponse("You've already signed up!")
	else:
		return HttpResponse("This event is full!")

def un_sign(request, pk):
	event = Event.objects.get(pk=pk)
	try:
		student = Student.objects.get(email=request.session['user'])
	except:
		return HttpResponseRedirect('/log_in/')
	if student in event.current_students.all():
		event.current_students.remove(student)
		event.save()
		return HttpResponseRedirect("/{}/".format(pk))
	else:
		return HttpResponse("You haven't signed up for this event!")

def cur_stud(request,pk):
	request.session['post_log'] = '/'
	event = Event.objects.get(pk=pk)
	try:
		student = Student.objects.get(email=request.session['user'])
	except:
		request.session['post_log'] = '/{}/students'.format(pk)
		return HttpResponseRedirect('/log_in/')
	students = event.current_students.all()
	names = []
	emails = {}
	officer = student.is_officer
	for s in students:
		names.append(s.__unicode__())
		emails[s.__unicode__()]=s.email
	back = '/{}/'.format(pk)
	return render_to_response('events/cur_stud.html', {'namesx':names, 'emailsx':emails, 'officer':officer, 'back':back})

def log_out(request):
	request.session['user'] = None
	return HttpResponseRedirect('/')

def my_events(request, year, month):
	myYear = int(year)
	myMonth = int(month)
	request.session['post_log'] = '/'
	try:
		student = Student.objects.get(email=request.session['user'])
	except:
		request.session['post_log'] = '/{0}/{1}/my_events/'.format(myYear, myMonth)
		return HttpResponseRedirect('/log_in/')
	try:
		student = Student.objects.get(email=request.session['user'])
	except:
		student = None
	events = Event.objects.order_by('start_time').filter(
		date__year=myYear, date__month=myMonth, current_students=student)
	cal = EventCalendar(events, student).formatmonth(myYear,myMonth)
	if myMonth == 12:
		nextMonth = 1
		nextYear = myYear+1
	else:
		nextYear = myYear
		nextMonth = myMonth+1
	nextUrl = '/{0}/{1}/my_events'.format(nextYear, nextMonth)

	if myMonth == 1:
		prevMonth = 12
		prevYear = myYear-1
	else:
		prevYear = myYear
		prevMonth = myMonth-1
	prevUrl = '/{0}/{1}/my_events'.format(prevYear, prevMonth)
	request.session['myev'] = True
	return render_to_response('events/calendar.html', {'calendar':mark_safe(cal), 'next':nextUrl, 'prev':prevUrl})

def edit_event(request,pk):
	try:
		student = Student.objects.get(email=request.session['user'])
	except:
		return HttpResponseRedirect('/log_in/')
	if not student.is_officer:
		return HttpResponse("You need to be an officer to see this page")
	event = Event.objects.get(pk=pk)
	if request.method == 'POST':
		form = EventForm(request.POST, instance=event)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/{}/'.format(pk))
	else:
		form = EventForm(instance=event)

	return render(request, 'events/edit.html', {'form': form, 'pk':pk})

def delete_event(request, pk):
	try:
		student = Student.objects.get(email=request.session['user'])
	except:
		return HttpResponseRedirect('/log_in/')
	if not student.is_officer:
		return HttpResponse("You need to be an officer")
	Event.objects.get(pk=pk).delete()
	return HttpResponseRedirect('/')
def profile(request):
	try:
		student = Student.objects.get(email=request.session['user'])
	except:
		return HttpResponseRedirect('/log_in/')
	events = Event.objects.order_by('date').filter(current_students=student)
	return render(request, 'events/profile.html', {'second':student.is_second_year, 'events':events},
		context_instance=RequestContext(request))

def update():
	events = Event.objects.all()
	students = Student.objects.all()
	for e in events:
		e.save()
	for s in students:
		s.save()