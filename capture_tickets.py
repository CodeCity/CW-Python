"""
	Author: Aaron Arlotti

	Python Script for use with ConnectWise
	Python Version: 3.5

	Description: The script will parse the tickets of a service board and select
	certain tickets based on a keyword. The tickets are then assigned to the user
	indicated in the script. The ticket is then moved to another service board.

"""

from time import strftime
import datetime as DT
import requests
import json


class AssignTicket:

	keyword = input("Keyword: ")

	url = "https://- CW URL -/v4_6_release/apis/3.0/"


	header = {
		'authorization': API_KEY,
		'content-type': "application/json",
		'cache-control': "no-cache"
	}

	def __init__(self):
		self.ticket_number = []

	def get_tickets():

		service_tickets = "service/tickets"

		querystring = {
			"orderBy": "dateEntered desc"
		}

		# connect to the server and get the tickets
		response = requests.get(
			url=AssignTicket.url + service_tickets, headers=AssignTicket.header, params=querystring)

		tickets = json.loads(response.text)

		for i in tickets:

			# parse the tickets for the specific service board.
			if i['board']['name'] == "GFI Max":

				# narrow down results to tickets that only have the keyword in the summary
				if AssignTicket.keyword in i['summary']:

					# print out the ticket - Ticket Number - Company Name - Status - Summary
					print(i['id'], i['summary'])

					# isolate the ticket number to pass to the other functions
					ticket_number = i['id']

					AssignTicket.schedule(ticket_number)
					AssignTicket.update(ticket_number)


	def schedule(ticket_number):

		'''
		TESTING HOW CW NEEDS TO ENTER TIME
		CW wants the time entered in a specific format.
		You can only add tickets during office hours.
		The different entries below were being used as I was testing over the weekend
		and before and after our office hours. I will leave them here so you can see
		how the time was adjusted.
		'''

		# Add or subtract a few hours depending if it is before or after office hours.
		time = DT.datetime.now()
		later = DT.timedelta(hours=2)
		add_hours = time + later

		today = time.strftime("%Y-%m-%dT%H:%M:%SZ")

		# Add a day or two depending if Sat or Sunday
		one_day = DT.timedelta(days=1)
		plus_one = time + one_day
		weekend = plus_one.strftime("%Y-%m-%dT%H:%M:%SZ")

		sched = "schedule/entries"

		schedule_entry = {
			"objectId": ticket_number,
			"member": {
				"identifier": "user1" # add your username here
			},
			"dateStart": today,
			"dateEnd": today,
			"where": {
            	"id": 4
			},
			"reminder": {
				"id": 1
			},
			"status": {
				"id": 2
			},
			"type": {
				"id": 4
			},
			"span": {
				"id": 2
			},
			"doneFlag": False,
			"acknowledgedFlag": True,
			"hours": .5
		}

		# get the ticket
		response = requests.request(
			"POST", AssignTicket.url + sched, headers=AssignTicket.header, json=schedule_entry,)
		# parse the response code
		rcode = response.status_code
		print(rcode)

		if rcode == 201:
			print("Ticket Scheduled")

		if rcode == 400:
			print(response.json())

		if rcode == 404:
			print("There is no ticket number " + ticket_number)

	def update(ticket_number):

		board = "service/tickets/" + str(ticket_number)

		payload = [
			{"op": "replace", "path": "/board/id", "value": 1},   # Support board
			{"op": "replace", "path": "/status/id", "value": 16}, # Status = New
			{"op": "replace", "path": "/team/id", "value": 20},   # Full Team
			{"op": "replace", "path": "/contact/name", "value": "Server Notification"}
		]

		print(url + board)

		r = requests.patch(
			url + board, headers=AssignTicket.header, data=json.dumps(payload))

		if r.status_code == 200:
			print("Ticket moved")

AssignTicket.get_tickets()


