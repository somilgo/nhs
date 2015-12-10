from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
import datetime
from django.core.validators import RegexValidator
import string
# Create your models here.

class StudentManager(BaseUserManager):
	def create_user(self, firstname, lastname, email, is_second_year, password, is_officer=False, hours=0, points=0):
		if not email:
			raise ValueError("Student must have an email address.")

		newStudent = self.model(
			email = self.normalize_email(email),
			firstname=firstname,
			lastname=lastname,
			is_officer=is_officer,
			is_second_year=is_second_year,
			hours=hours,
			points=points
		)

		newStudent.set_password(password)
		user.save(using=self.db)
		return newStudent
	def create_superuser(self, firstname, lastname, email, password, is_second_year, is_officer=True, hours=0, points=0):
		newSuperStudent = self.create_user(
			email = self.normalize_email(email),
			firstname=firstname,
			lastname=lastname,
			is_officer=is_officer,
			is_second_year=is_second_year,
			hours=hours,
			points=points,
			password=password
		)
		newSuperStudent.is_admin = True
		newSuperStudent.save(using=self.db)
		return newSuperStudent


class Student(AbstractBaseUser):
	objects = StudentManager()
	firstname = models.CharField(verbose_name="First Name", max_length=30, default="")
	lastname = models.CharField(verbose_name="Last Name", max_length=30, default="")
	email = models.EmailField(
		verbose_name='Email Address',
		max_length=255,
		unique=True,
		default=''
	)
	is_officer = models.BooleanField(default=False)
	is_second_year = models.BooleanField(verbose_name="Check this box if you are a SENIOR")
	hours = models.DecimalField(max_digits=10, decimal_places=2, default=0)
	points = models.DecimalField(max_digits=10, decimal_places=1, default=0)
	required_hours = models.DecimalField(max_digits=3, decimal_places=1, default = 12)
	phone_regex = RegexValidator(regex=r'^[1-9]\d{2}-\d{3}-\d{4}$', message="Phone number must be entered in the format: 'XXX-XXX-XXXX'")
	phone = models.CharField(validators=[phone_regex], verbose_name="Phone Number", max_length=12, default = '000-000-0000')
	USERNAME_FIELD = 'email'

	def __unicode__(self):
		return self.firstname + " " + self.lastname
	def save(self):
		events = Event.objects.order_by('date').filter(current_students=self)
		hourz = 0
		pointz = 0
		for i in events:
			if i.event_completed:
				hourz+=i.total_hours
				pointz+=i.total_points
		self.hours = hourz
		self.points = pointz
		super(Student, self).save()

class Event(models.Model):
	current_students = models.ManyToManyField(Student, blank=True)
	name = models.CharField(max_length=200)
	location = models.CharField(max_length=200)
	date = models.DateField()
	start_time = models.TimeField()
	end_time = models.TimeField()
	total_hours = models.DecimalField(max_digits=4, decimal_places=2)
	total_points = models.DecimalField(max_digits=3, decimal_places=1, default=0)
	max_students = models.IntegerField()
	num_students = models.IntegerField()
	event_description = models.TextField(default='')
	event_completed = models.BooleanField(default=False)

	def save(self):
		namex = self.name
		namex = filter(lambda x: x in string.printable, namex)
		self.name = namex
		dateTimeEnd = datetime.datetime.combine(self.date, self.end_time)
		if dateTimeEnd < datetime.datetime.now():
			self.event_completed=True
		else:
			self.event_completed=False
		try:
			self.num_students = len(self.current_students.all())
		except:
			self.num_students = 0
		super(Event, self).save()

	def get_absolute_url(self):
		return "/{}/".format(self.pk)

	def __unicode__(self):
		return self.name