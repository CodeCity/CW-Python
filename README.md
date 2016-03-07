## Scripts for ConnectWise ##

#### Description ####

The ConnectWise UI is a bit bloated. These scripts are intended to perform quick tasks without having to be in the interface.  


**Review each script and test it with your own Training account before trying them with your live data.** 

User accepts all responsibility. 


#### Scripts ####


* [Add Time to a Ticket](https://github.com/CodeCity/CW-Python/blob/master/add_time_to_a_ticket.py)
	* A script to enter time to a specific ticket. 
		* Update the script with your own info. 
			* Enter the Service Ticket number.
			* Enter the Actual Hours.
			* Enter the notes. 

* [Automatically Delete Tickets](https://github.com/CodeCity/CW-Python/blob/master/auto_ticket_deletion.py)

I have no IMAP access to the company server so I forward the emails to a Gmail account. 
Once the emails are in the Gmail inbox, the script parses the subject lines of the emails. 
* Currently, the subject line is: Ticket (ticketnumber) has been deleted. 
	* The subject is parsed and the ticket number is found. 
	* The ticket is deleted. 
		* If the ticket has any other status other than >Delete Ticket, it will not be removed. 
	* The email is then moved to the Trash

