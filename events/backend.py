from events.models import Student
from django.contrib.auth.hashers import check_password

class StudentBackend(object):

	def authenticate(self, email=None, password=None):
		stud = Student.objects.filter(email=email)
		if stud.exists():
			if check_password(password, stud[0].password):
				return stud[0]
		return None
	def get_user(self, email):
		stud = Student.objects.filter(email=email)
		if stud.exists():
			return stud[0]
		else:
			return None