#!/usr/bin/env python
from __future__ import unicode_literals
from time import sleep, time
import requests
import io
import smtplib
from smtp_config import sender, password, receivers, host, port, message


DELAY = 60  # Delay between site queries
EMAIL_INTERVAL = 1800  # Delay between alert emails


def monitor(SITE, email_time):
    resp = requests.get(SITE)
    if resp.status_code != 200:
        print "{} status: {}".format(SITE, resp.status_code)
        # If more than EMAIL_INTERVAL seconds since last email, resend
        if (time() - email_time[SITE]) > EMAIL_INTERVAL:
            try:
                smtpObj = smtplib.SMTP(host, port) # Set up SMTP object
                smtpObj.starttls()
                smtpObj.login(sender, password)
                smtpObj.sendmail(sender, receivers, message)
                email_time[SITE] = time()
                print "Successfully sent email"
            except smtplib.SMTPException:
                print "Error sending email ({}:{})".format(host, port)


if __name__ == '__main__':
    # Read in sites to monitor
    SITES = [site.strip() for site in io.open('sites.txt', mode='r').readlines()]
    email_time = {}

    for SITE in SITES:
        print "Beginning monitoring of {}".format(SITE)
        email_time[SITE] = 0

    while True:
        try:
            for SITE in SITES:
                monitor(SITE, email_time)
            sleep(DELAY)
        except KeyboardInterrupt:
            print "\n-- Monitoring canceled --"
            break
