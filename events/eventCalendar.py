from calendar import HTMLCalendar
from datetime import date
from itertools import groupby
from models import *
from django.utils.html import conditional_escape as esc

class EventCalendar(HTMLCalendar):

	def __init__(self, events, student):
		super(EventCalendar, self).__init__()
		self.events = self.group_by_day(events)
		self.student = student

	def formatday(self, day, weekday):
		try:
			doneevents = Event.objects.order_by('date').filter(current_students=self.student)
		except:
			doneevents = []
		if day != 0:
			cssclass = self.cssclasses[weekday]
			if date.today() == date(self.year, self.month, day):
				cssclass += ' today'
			if day in self.events:
				cssclass += ' filled'
				body = ['<ul>']
				for event in self.events[day]:
					if event in doneevents and event.event_completed:
						aClass = "green"
					elif event in doneevents and not event.event_completed:
						aClass = "yellow"
					elif event not in doneevents and event.event_completed:
						aClass = "white"
					else:
						aClass = "cyan"
						if event.num_students >= event.max_students:
							aClass = 'red'
					body.append('<li>')
					body.append('<a href="%s" style="color:%s">' % (event.get_absolute_url(), aClass))
					body.append(esc(event.name))
					body.append('</a></li>')
				body.append('</ul>')
				return self.day_cell(cssclass, '%d %s' % (day, ''.join(body)))
			return self.day_cell(cssclass, day)
		return self.day_cell('noday', '&nbsp;')

	def formatmonth(self, year, month):
		self.year, self.month = year, month
		return super(EventCalendar, self).formatmonth(year, month)

	def group_by_day(self, events):
		field = lambda event: event.date.day
		return dict(
			[(day, list(items)) for day, items in groupby(events, field)]
		)

	def day_cell(self, cssclass, body):
		return '<td class="{0}"><div style=\"min-height:100px;\">{1}</div></td>'.format(cssclass, body)