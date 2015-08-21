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

# Create your views here.

def home(request):
	return HttpResponse("This is the home page!")

def sign_up(request):
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/sign_up_success/')
	else:
		form = RegistrationForm()

	return render(request, 'events/sign_up.html', {'form': form})

def sign_up_success(request):
	return HttpResponse("Thanks for signing up!")

def log_in(request):
	form = LogIn(request.POST or None)

	if form.is_valid():
		email = form.cleaned_data['email']
		password = form.cleaned_data['password']
		user = authenticate(email=email, password=password)
		if user is not None:
			login(request, user)
			request.session['user'] = email
			return HttpResponseRedirect(reverse('events:log_in_success'))
		else:
			messages.warning(request, "Username or password is incorrect.")
	return render(request, 'events/log_in.html', {'form':form})

def log_in_success(request):
	return HttpResponse("{} has logged in!".format(request.session['user']))

def event_creator(request):
	if request.method == 'POST':
		form = EventForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/event_success/')
	else:
		form = EventForm()

	return render(request, 'events/event_creator.html', {'form': form})

def event_success(request):
	return HttpResponse("Your event has been successfully created!")

class EventDetailView(DetailView):
	model = Event

def event_details(request, pk):
	event = Event.objects.get(pk=pk)
	student = Student.objects.get(email=request.session['user'])
	signed_up = False
	full = True
	print "money"
	if student in event.current_students.all():
		signed_up = True
		print "money"
	if event.num_students < event.max_students:
		full = False
	return render_to_response('events/event_detail.html', {'object':event, 'full':full, 'signed_up':signed_up})

def calendar(request, year, month):
	myYear = int(year)
	myMonth = int(month)
	events = Event.objects.order_by('date').filter(
		date__year=myYear, date__month=myMonth)
	cal = EventCalendar(events).formatmonth(myYear,myMonth)
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
			return HttpResponse("Thanks for signing up!")
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
		return HttpResponse("You've unsigned up")
	else:
		return HttpResponse("You haven't signed up!")
