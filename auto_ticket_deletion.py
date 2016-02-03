""" 
 Author: Aaron Arlotti 
 ConnectWise Python Script 

 Delete tickets automatically. 
 
 Deleted tickets are forwarded to a Gmail account. 
 The script parses the Gmail and finds the ticket number,
 checks the ticket if the status is Delete Ticket, and then 
 Deletes or ignores the ticket. The email is then moved to 
 the Trash
 
""" 


import imaplib
import requests
import json
import re
import time
import sys


def autoTicketDeletion():

    # get email from the gmail account
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login('GMAIL_ADDRESS', 'GMAIL_PASSWORD')
    mail.select("inbox")

    result, data = mail.search(None, 'SUBJECT', 'Ticket')


    # if there are no emails
    if '' in data:
        print("There are no emails.")
        sys.exit()
    # if there are emails with 'Ticket' in the subject...
    else:
        mail.recent()
        # find email ids
        ids = data[0]
        # put ids in a space separated string
        id_list = ids.split()

        for latest_email_id in id_list:
            # get the full email body
            result, email_body = mail.fetch(latest_email_id, "(RFC822)")

            # get the raw email, and find the ticket number.
            raw_email = email_body[0][1]

            # parse for the specific emails with a ticket number.
            # check the regex for your ticket numbers. Our current tickets are 300000
            ticket_string = re.compile(r'(3\d{5}).+(?:has been deleted)')
            ticket_numbers = ticket_string.findall(raw_email)
            ticket_number = ticket_numbers[0]

            # enter the URL of your CW server. 
            url = "https:// -URL OF CONNECTWISE SERVER- /v4_6_release/apis/3.0/service/tickets/" + ticket_number

            headers = {
            # CW API keys = Company+Public:Private keys
            'authorization': "API_KEY",
            'content-type': "application/json",
            'cache-control': "no-cache",
            }

            response = requests.request("GET", url, headers=headers)
            # get the response code
            rcode = response.status_code

            # if the CW ticket exists
            if rcode == 200:
                json_string = response.text
                parsed_json = json.loads(json_string)

                # parse the ticket status. 'New', 'In Progress', '>Delete Ticket', etc.
                status = (parsed_json['status']['name'])

                # if ticket it is any other status than Delete Ticket or Customer Cancelled, 
                # the ticket will not be deleted. 
                if status == '>Delete Ticket' or '>Customer Cancelled':
                    print('Ticket number: ' + ticket_number + ' will be deleted.')
                    requests.request("DELETE", url, headers=headers)
                    print('Ticket ' + ticket_number + ' was deleted.')
                    
                    # the email is then moved to the Trash. 
                    mail.store(latest_email_id, '+X-GM-LABELS', '\\Trash')
                    mail.expunge()
                    time.sleep(5)
                elif status != '>Deleted Ticket':
                    print("Ticket " + ticket_number + " has the status of " + status + "\nDo you have the right ticket number?")
                    break

            # if the CW service ticket doesn't exist
            if rcode == 404:
                print("There is no ticket number " + ticket_number)
                print("Moving email to Trash")
                mail.store(latest_email_id, '+X-GM-LABELS', '\\Trash')
                mail.expunge()
                time.sleep(5)



autoTicketDeletion()




