from calendar import HTMLCalendar
from datetime import date
from itertools import groupby

from django.utils.html import conditional_escape as esc

class EventCalendar(HTMLCalendar):

	def __init__(self, events):
		super(EventCalendar, self).__init__()
		self.events = self.group_by_day(events)

	def formatday(self, day, weekday):
		if day != 0:
			cssclass = self.cssclasses[weekday]
			if date.today() == date(self.year, self.month, day):
				cssclass += ' today'
			if day in self.events:
				cssclass += ' filled'
				body = ['<ul>']
				for event in self.events[day]:
					body.append('<li>')
					body.append('<a href="%s">' % event.get_absolute_url())
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
		return '<td class="%s">%s</td>' % (cssclass, body)