from datetime import datetime, timedelta
from utils import process_calendar
from capabilities import check_availability, query_functionality, busy_day

calendars = []

endpoint = input("""
Welcome to HouseWhisper Calendar helper!\n\n
Our API offers the following endpoints:\n
\t- POST /new_calendar -path
\t- GET /check_availability/<agent_id> -datetime
\t- GET /query_functionality/<agent_id> -start -end -duration -n
\t- GET /busy_day/<agent_id> -date\n\n\n
To exit please press enter\n
-->\t""").strip("/")

while len(endpoint):
	try:
		if endpoint.startswith("new"):
			path = input("-path ")
			calendars.append(process_calendar(path))
			print("Calendar added for agent_id:", len(calendars))
		elif endpoint.startswith("check"):
			agent_id = int(endpoint.split("/")[1])
			given_time = input("Please use format %m/%d/%Y %H:%M\n-given_time ")
			while len(given_time) > 0:
				print(check_availability(
						calendars[agent_id - 1],
						datetime.strptime(given_time,
						"%m/%d/%Y %H:%M").astimezone()))
				given_time = input("-given_time ")
		elif endpoint.startswith("query"):
			agent_id = int(endpoint.split("/")[1])
			start = datetime.strptime(input("-start "), "%m/%d/%Y %H:%M").astimezone()
			end = datetime.strptime(input("-end "), "%m/%d/%Y %H:%M").astimezone()
			duration = timedelta(minutes=int(input("-duration ")))
			n = int(input("-n "))
			query_functionality(calendars[agent_id - 1], start, end, duration, n)
		elif endpoint.startswith("busy"):
			agent_id = int(endpoint.split("/")[1])
			date = datetime.strptime(input("-date ") + " 08:00", "%m/%d/%Y %H:%M").astimezone()
			busy_day(calendars[agent_id - 1], date)
		else:
			raise Exception
		endpoint = input("-->\t").strip("/")
	except Exception as err:
		print("400 Bad Request\n", err)
		endpoint = input("-->\t").strip("/")


"""
Examples:

/new_calendar
data/jhasardr@gmail.com.ics
/check_availability/1
2/10/2025 20:00
2/10/2025 10:00
2/10/2025 12:00
2/10/2025 09:00

/query_functionality/1
2/10/2025 09:00
2/12/2025 20:00
60
5

/new_calendar
data/jhasardr@gmail.com.ics
/busy_day/1
2/11/2025
2/10/2025


/new_calendar
data/jhasardr@gmail.com.ics
/query_functionality/2
2/10/2025 09:00
2/12/2025 20:00
15
5

"""