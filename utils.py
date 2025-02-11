from icalendar import Calendar
from datetime import timedelta, datetime

def process_calendar(path: str) -> dict[str, str]:
	parsed_calendar = {}
	with open(path, 'rb') as file:
		calendar = Calendar.from_ical(file.read())
		for event in calendar.walk("VEVENT"):
			start = event.decoded("dtstart")
			now = datetime.now().date()
			if type(start) != type(now):
				start = start.date()
			if start >= now:
				starting = discretize(event.decoded("dtstart").astimezone())
				ending = event.decoded("dtend").astimezone()
				while starting < ending:
					parsed_calendar[starting] = event.get("summary")
					starting += timedelta(minutes=15)
	return parsed_calendar

# inspired by https://stackoverflow.com/questions/48937900/round-time-to-nearest-hour-python
def discretize(date: datetime) -> datetime:
	return date.replace(
					second=0,
					microsecond=0,
					minute=date.minute//15*15,
					hour=date.hour
				)

def check_timeframe(calendar: dict[str, str], current: datetime, duration: timedelta, end: datetime):
	free_duration = timedelta(minutes=15)
	while (
		current not in calendar
		and current < end - timedelta(minutes=15)
		and (current.hour < 19 or current.minute < 45)
	):
		current += timedelta(minutes=15)
		if current not in calendar:
			free_duration += timedelta(minutes=15)
	if free_duration >= duration:
		return free_duration
	return timedelta()

def check_timeframe_alt(calendar: dict[str, str], current: datetime, duration: timedelta) -> bool:
	free_duration = timedelta(minutes=15)
	while free_duration < duration and current not in calendar:
		current += timedelta(minutes=15)
		if current not in calendar:
			free_duration += timedelta(minutes=15)
	if free_duration >= duration:
		return True
	return False

def pretty_datetime(date_time: datetime) -> str:
	return date_time.strftime("%m/%d/%Y %H:%M")
