# -*- coding: utf-8 -*-
"""
Author: Aaron Arlotti

ConnectWise Python Script
Enterting time on a ticket. 

Streamlined script, only asks for 
Ticket number, Amount of time to bill, and the notes. 

Does not check if there is existing time on the ticket.

"""

import datetime
import requests
import json


ticket_number = raw_input('Ticket number: ')
actual_hours = raw_input('Actual hours: ')
notes = raw_input('Notes: ')
today = datetime.date.today().isoformat()

# Add the URL TO YOUR SERVER
addTime = "https://-URL TO YOUR SERVER-/v4_6_release/apis/3.0/time/entries"

header = {
# Add your Company+Public:Private keys. 
'authorization': "API_KEYS",
'content-type': "application/json",
'cache-control': "no-cache",
}


time_entry = {
        'chargeToId': ticket_number,
        'chargeToType': 'ServiceTicket',
        # Enter your CW Username - User1 used for company "Training"  
        'member': {"identifier": "User1"},
        'timeStart': today,
        'actualHours': actual_hours,
        'billableOption': 'Billable',
        'notes': notes,

    }


t = requests.post(addTime, headers=header, json=time_entry)

result = t.status_code

if result == 201:
    print("Success")
else:
    print("TIME NOT ENTERED")