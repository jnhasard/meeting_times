from datetime import timedelta, datetime
from utils import discretize, check_timeframe, pretty_datetime

def check_availability(calendar: dict[str, str], given_time: datetime) -> bool:
	given_time = discretize(given_time)
	if given_time not in calendar:
		if given_time + timedelta(minutes=15) in calendar:
			print("Warning: 15 or less minutes free")
		return True
	return False

def query_functionality(
		calendar: dict[str, str],
		start: datetime,
		end: datetime,
		duration: timedelta,
		n: int
	)-> list[datetime]:
	free_times = []
	current = discretize(start)
	end = discretize(end + timedelta(minutes=14))
	while current < end and n > 0:
		if current.hour >= 20:
			current = current.replace(
					minute=0,
					hour=8,
					day=current.day + 1
				)
		if current in calendar:
			current += timedelta(minutes=15)
			continue
		else:
			if current + duration < end:
				amount = check_timeframe(calendar, current, duration, end)
				if amount >= duration:
					n -= 1
					free_times.append((current, amount))
					print(
						len(free_times),
						"-> You got time from:",
						pretty_datetime(current),
						"to",
						pretty_datetime(current + amount)
					)
					current += amount
				else:
					current += timedelta(minutes=15)
			else:
				break
	return free_times

def busy_day(calendar: dict[str, str], day: datetime) -> datetime:
	free_time = query_functionality(calendar, day, day + timedelta(hours=12), timedelta(minutes=90), 1)
	if len(free_time) > 0:
		return free_time[0]
	return None
