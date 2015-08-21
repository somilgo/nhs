from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
import datetime

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
	is_second_year = models.BooleanField(verbose_name="Check this box if this is your second year in NHS")
	hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)
	points = models.DecimalField(max_digits=3, decimal_places=1, default=0)

	USERNAME_FIELD = 'email'

	def __unicode__(self):
		return self.firstname + " " + self.lastname

class Event(models.Model):
	current_students = models.ManyToManyField(Student, blank=True)
	name = models.CharField(max_length=200)
	location = models.CharField(max_length=200)
	date = models.DateField()
	start_time = models.TimeField()
	end_time = models.TimeField()
	total_hours = models.DecimalField(max_digits=4, decimal_places=2)
	total_points = models.DecimalField(max_digits=3, decimal_places=1)
	max_students = models.IntegerField()
	num_students = models.IntegerField()
	event_description = models.TextField(default='')
	event_completed = models.BooleanField(default=False)

	def save(self):
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