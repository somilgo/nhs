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
import decimal
import csv
from django.contrib.auth.models import User
import os

# Create your views here.
import random
random.seed()

def reset(request):
	from django.core.management import call_command
	call_command('flush', interactive=False)
	username = os.environ.get("SUPERNAME")
	u = User(username=username)
	u.set_password(username)
	u.is_superuser = True
	u.is_staff = True
	u.save()
	return HttpResponse("The database has been reset")

def home(request):
	from django.contrib.sessions.models import Session
	current = request.session.session_key
	allsess = Session.objects.exclude(session_key=current)
	print "There are currently {} sessions".format(len(allsess))
	if len(allsess) > 1000:
		allsess.delete()

	request.session['post_log'] = '/'
	try:
		student = Student.objects.get(email=request.session['user'])
		logged = True
	except:
		logged = False
		student = None
	try:
		request.session['update']
	except:
		update()
		request.session['update'] = 0
	if logged:
		if student.phone == '000-000-0000':
			return HttpResponseRedirect('/phone_input/')
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

def change_pass(request):
	form = ChangePass(request.POST or None)
	if form.is_valid():
		password = form.cleaned_data['password1']
		try:
			student = Student.objects.get(email=request.session['user'])
		except:
			return HttpResponseRedirect('/log_in/')
		try:
			student = Student.objects.get(email=request.session['prof'])
		except:
			return HttpResponseRedirect('/')
		student.set_password(password)
		student.save()
		return HttpResponseRedirect('/')
	return render(request, 'events/pass.html', {'form':form})

def change_phone(request):
	form = PhoneInput(request.POST or None)
	if form.is_valid():
		phonenum = form.cleaned_data['phone']
		try:
			student = Student.objects.get(email=request.session['user'])
		except:
			return HttpResponseRedirect('/log_in/')
		student.phone = phonenum
		student.save()
		return HttpResponseRedirect('/')
	return render(request, 'events/phone.html', {'form':form})

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
	events = Event.objects.order_by('date').filter(
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
	emails = []
	officer = student.is_officer
	for s in students:
		temp = []
		names.append(s.__unicode__())
		temp.append(s.__unicode__())
		temp.append(s.email)
		temp.append(s.phone)
		temp.append(s.pk)
		emails.append(temp)
	back = '/{}/'.format(pk)
	return render_to_response('events/cur_stud.html', {'namesx':names, 'emailsx':emails, 'officer':officer, 'back':back, 'eventpk':pk})

def log_out(request):
	request.session.flush()
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

def dup_event(request,pk):
	try:
		student = Student.objects.get(email=request.session['user'])
	except:
		return HttpResponseRedirect('/log_in/')
	if not student.is_officer:
		return HttpResponse("You need to be an officer to see this page")
	event = Event.objects.get(pk=pk)
	if request.method == 'POST':
		form = DupEventForm(request.POST, instance=event)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/{}/'.format(pk))
	else:
		form = DupEventForm(instance=event)

	return render(request, 'events/duplicate.html', {'form': form, 'pk':pk})

def delete_event(request, pk):
	try:
		student = Student.objects.get(email=request.session['user'])
	except:
		return HttpResponseRedirect('/log_in/')
	if not student.is_officer:
		return HttpResponse("You need to be an officer to view this page!")
	Event.objects.get(pk=pk).delete()
	return HttpResponseRedirect('/')
def profile(request):
	try:
		student = Student.objects.get(email=request.session['user'])
		request.session['prof'] = request.session['user']
	except:
		return HttpResponseRedirect('/log_in/')
	events = Event.objects.order_by('date').filter(current_students=student)
	supers = False
	return render(request, 'events/profile.html', {'events':events, 'supers':supers},
		context_instance=RequestContext(request))

def remove_student(request, eventpk, studentpk):
	try:
		student = Student.objects.get(email=request.session['user'])
	except:
		return HttpResponseRedirect('/log_in/')
	if not student.is_officer:
		return HttpResponse("You need to be an officer to view this page!")
	event = Event.objects.get(pk=eventpk)
	student_to_remove = Student.objects.get(pk=studentpk)
	if student_to_remove in event.current_students.all():
		event.current_students.remove(student_to_remove)
		event.save()
		return HttpResponseRedirect("/{}/students".format(eventpk))
	else:
		return HttpResponse("This student is no longer signed up for this event!")

def delete_student(request, pk):
	try:
		student = Student.objects.get(email=request.session['user'])
	except:
		return HttpResponseRedirect('/log_in/')
	if not student.is_officer:
		return HttpResponse("You need to be an officer to view this page!")
	student_to_delete = Student.objects.get(pk=pk)
	student_to_delete.delete()
	update()
	return HttpResponseRedirect('/students_list/')

def student_list(request):
	try:
		student = Student.objects.get(email=request.session['user'])
	except:
		return HttpResponseRedirect('/log_in/')
	if not student.is_officer:
		return HttpResponse("You need to be an officer to view this page!")
	allStuds = Student.objects.all()

	return render_to_response('events/students.html', {'students':allStuds})

def super_profile(request, pk):
	try:
		student = Student.objects.get(email=request.session['user'])
	except:
		return HttpResponseRedirect('/log_in/')
	if not student.is_officer:
		return HttpResponse("You need to be an officer to view this page!")
	student = Student.objects.get(pk=pk)
	request.session['prof'] = student.email
	events = Event.objects.order_by('date').filter(current_students=student)
	supers = True
	return render(request, 'events/profile.html', { 'events':events, 'supers':supers, 'student':student, 'pk':pk})

def add_req(request, pk):
	try:
		student = Student.objects.get(email=request.session['user'])
	except:
		return HttpResponseRedirect('/log_in/')
	if not student.is_officer:
		return HttpResponse("You need to be an officer to view this page!")
	student = Student.objects.get(pk=pk)
	student.required_hours = student.required_hours + decimal.Decimal(.5)
	student.save()
	return HttpResponseRedirect('/students_list/' + pk)

def min_req(request, pk):
	try:
		student = Student.objects.get(email=request.session['user'])
	except:
		return HttpResponseRedirect('/log_in/')
	if not student.is_officer:
		return HttpResponse("You need to be an officer to view this page!")
	student = Student.objects.get(pk=pk)
	student.required_hours = student.required_hours - decimal.Decimal(.5)
	student.save()
	return HttpResponseRedirect('/students_list/' + pk)

def add_out(request, pk):
	try:
		student = Student.objects.get(email=request.session['user'])
	except:
		return HttpResponseRedirect('/log_in/')
	if not student.is_officer:
		return HttpResponse("You need to be an officer to view this page!")
	student = Student.objects.get(pk=pk)
	student.addedHours = student.addedHours + decimal.Decimal(.5)
	student.save()
	return HttpResponseRedirect('/students_list/' + pk)

def sub_out(request, pk):
	try:
		student = Student.objects.get(email=request.session['user'])
	except:
		return HttpResponseRedirect('/log_in/')
	if not student.is_officer:
		return HttpResponse("You need to be an officer to view this page!")
	student = Student.objects.get(pk=pk)
	student.addedHours = student.addedHours - decimal.Decimal(.5)
	student.save()
	return HttpResponseRedirect('/students_list/' + pk)


def outputEvents(request):
	try:
		student = Student.objects.get(email=request.session['user'])
	except:
		return HttpResponseRedirect('/log_in/')
	if not student.is_officer:
		return HttpResponse("You need to be an officer to view this page!")

	response = HttpResponse(content_type='text/csv')
	date = datetime.datetime.today().strftime('%Y-%m-%d')
	response['Content-Disposition'] = 'attachment; filename="events_{}.csv"'.format(str(date))

	writer = csv.writer(response)

	events = Event.objects.order_by('date')
	for e in events:
		eventunit = []
		eventunit.append(str(e.date))
		eventunit.append(str(e.start_time))
		eventunit.append(str(e.name))
		for s in e.current_students.all():
			eventunit.append(str(s))
		writer.writerow(eventunit)

	return response

def update():
	events = Event.objects.all()
	students = Student.objects.all()
	for e in events:
		e.save()
	for s in students:
		s.save()