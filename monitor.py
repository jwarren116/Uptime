#!/usr/bin/env python
from __future__ import unicode_literals
from time import sleep, time, strftime
import requests
import io
import smtplib
import sys
from smtp_config import sender, password, receivers, host, port


DELAY = 60  # Delay between site queries
EMAIL_INTERVAL = 1800  # Delay between alert emails

# Define escape sequences for colored terminal output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BOLD = "\033[1m"
END = "\033[0m"

# Message template for alert
message = """From: {sender}
To: {receivers}
Subject: Monitor Service Notification

You are being notified that {SITE} is experiencing a {status} status!
"""


def monitor(SITE, email_time):
    resp = requests.get(SITE)
    if resp.status_code == 200:
        print "\b" + GREEN + "." + END,
        sys.stdout.flush()
    else:
        print "\n({}) {} {}STATUS: {}{}".format(strftime("%a %b %d %Y %H:%M:%S"),
                                                SITE,
                                                YELLOW,
                                                resp.status_code,
                                                END
                                                )
        # If more than EMAIL_INTERVAL seconds since last email, resend
        if (time() - email_time[SITE]) > EMAIL_INTERVAL:
            try:
                smtpObj = smtplib.SMTP(host, port)  # Set up SMTP object
                smtpObj.starttls()
                smtpObj.login(sender, password)
                smtpObj.sendmail(sender,
                                 receivers,
                                 message.format(sender=sender,
                                                receivers=", ".join(receivers),
                                                SITE=SITE,
                                                status=resp.status_code
                                                )
                                 )
                email_time[SITE] = time()  # Update time of last email
                print GREEN + "Successfully sent email" + END
            except smtplib.SMTPException:
                print RED + "Error sending email ({}:{})".format(host, port) + END


if __name__ == '__main__':
    # Accept sites from command line input
    SITES = sys.argv[1:]

    # Read in additional sites to monitor from sites.txt file
    try:
        SITES += [site.strip() for site in io.open('sites.txt', mode='r').readlines()]
    except IOError:
        print RED + "No sites.txt file found" + END

    email_time = {}  # Monitored sites and timestamp of last alert sent

    for SITE in SITES:
        print BOLD + "Beginning monitoring of {}".format(SITE) + END
        email_time[SITE] = 0  # Initialize timestamp as 0

    while True:
        try:
            for SITE in SITES:
                monitor(SITE, email_time)
            sleep(DELAY)
        except KeyboardInterrupt:
            print RED + "\n-- Monitoring canceled --" + END
            break
