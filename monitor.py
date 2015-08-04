#!/usr/bin/env python
from __future__ import unicode_literals
from time import sleep
import requests
import io
import smtplib
from smtp_config import sender, password, receivers, host, port, message

SITES = io.open('sites.txt', mode='r').readlines()
SITES = [site.strip() for site in SITES]

for SITE in SITES:
    print "Beginning monitoring of {}".format(SITE)

try:
    while True:
        resp = requests.get(SITES[0])
        if resp.status_code != 200:
            print "{} status: {}".format(SITES[0], resp.status_code)
            try:
                smtpObj = smtplib.SMTP(host, port)
                smtpObj.starttls()
                smtpObj.login(sender, password)
                smtpObj.sendmail(sender, receivers, message)
                print "Successfully sent email"
            except smtplib.SMTPException:
                print "Error sending email ({}:{})".format(host, port)
        sleep(3)
except KeyboardInterrupt:
    print "\n-- Monitoring canceled --"
