import datetime
from events.models import *

def nav(request):
	try:
		student = Student.objects.get(email=request.session['user'])
		logged = True
	except:
		logged = False
		student = None
	if request.get_full_path() == '/':
		not_home = False
	else:
		not_home = True
	return {'year': datetime.datetime.now().year,
	 'month': datetime.datetime.now().month, 'student': student, 'logged':logged, 'not_home':not_home}