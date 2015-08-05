#!/usr/bin/env python
from __future__ import unicode_literals
from time import sleep, time
import requests
import io
import smtplib
from smtp_config import sender, password, receivers, host, port, message

SITES = io.open('sites.txt', mode='r').readlines()
SITES = [site.strip() for site in SITES]

DELAY = 60 # Delay between site queries
EMAIL_INTERVAL = 1800 # Delay between alert emails

time_email_sent = 0

for SITE in SITES:
    print "Beginning monitoring of {}".format(SITE)

try:
    while True:
        resp = requests.get(SITES[0])
        if resp.status_code != 200:
            print "{} status: {}".format(SITES[0], resp.status_code)
            if (time() - time_email_sent) > EMAIL_INTERVAL:
                try:
                    smtpObj = smtplib.SMTP(host, port)
                    smtpObj.starttls()
                    smtpObj.login(sender, password)
                    smtpObj.sendmail(sender, receivers, message)
                    time_sent = time()
                    print "Successfully sent email"
                except smtplib.SMTPException:
                    print "Error sending email ({}:{})".format(host, port)
        sleep(DELAY)
except KeyboardInterrupt:
    print "\n-- Monitoring canceled --"
