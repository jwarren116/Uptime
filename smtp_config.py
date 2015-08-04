#!/usr/bin/env python

# Login email and password for account sending alerts
sender = "monitor@example.com"
password = "examplepassword"

# Mail domain and port for account sending alerts
host = "mail.example.com"
port = 587

# Recipients that will get alert
receivers = ['john.doe@gmail.com']

# Message template for alert
message = """From: {}
To: {}
Subject: Monitor Service Notification

Example notification text here!
""".format(sender, receivers)
