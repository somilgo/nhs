from django import forms
from events.models import *
from django.contrib.auth.hashers import check_password

class RegistrationForm(forms.ModelForm):
	"""
	Form for registering a new account.
	"""
	password1 = forms.CharField(widget=forms.PasswordInput,
								label="Password")
	password2 = forms.CharField(widget=forms.PasswordInput,
								label="Password (again)")
	class Meta:
		model = Student
		fields = ('firstname', 'lastname', 'email', 'password1', 'password2', 'is_second_year')

	def clean(self):
		# Check that the two password entries match
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		email = self.cleaned_data.get("email")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords don't match")
		if Student.objects.filter(email=email).exists():
			raise forms.ValidationError("This email has already been registered")
		return self.cleaned_data

	def save(self, commit=True):
		user = super(RegistrationForm, self).save(commit=False)
		user.set_password(self.cleaned_data['password1'])
		if commit:
			user.save()
		return user

class LogIn(forms.Form):
	email = forms.EmailField(label = "Email")
	password = forms.CharField(widget=forms.PasswordInput, label="Password")
	def clean(self):
		password = self.cleaned_data.get("password")
		email = self.cleaned_data.get("email")
		stud = Student.objects.filter(email=email)
		if (not (stud.exists())):
			raise forms.ValidationError("This email has not been registered")
		else:
			if check_password(password, stud[0].password):
				pass
			else:
				raise forms.ValidationError("Email and password combination do not match.")
		return self.cleaned_data

class ChangePass(forms.Form):
	password1 = forms.CharField(widget=forms.PasswordInput, label="New Password")
	password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
	def clean(self):
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 != password2:
			raise forms.ValidationError("Passwords do not match!")
		
		return self.cleaned_data


class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
	input_type = 'time'

class EventForm(forms.ModelForm):
	date = forms.DateField(widget=DateInput)
	start_time = forms.TimeField(widget=TimeInput)
	end_time = forms.TimeField(widget=TimeInput)
	current_students = forms.ModelMultipleChoiceField(queryset=Student.objects.all(),widget=forms.SelectMultiple,required=False)
	class Meta:
		model = Event
		exclude = ['num_students', 'event_completed', 'total_points']
	def clean(self):
		students = self.cleaned_data['current_students']
		self.cleaned_data['total_points'] = 0
		self.cleaned_data['num_students'] = len(students)
		self.cleaned_data['event_completed'] = False
		if len(students) > self.cleaned_data['max_students']:
			raise forms.ValidationError("There are more than the maximum number of students registered. Please increase the maximum or remove some students")

		return self.cleaned_data
	def save(self, commit=True):
		event = super(EventForm, self).save(commit=False)
		
		if commit:
			event.save()
		event.current_students = self.cleaned_data['current_students']
		event.save()
		return event




