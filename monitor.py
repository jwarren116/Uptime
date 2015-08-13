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


def main(SITE, email_time):
    resp = requests.get(SITE)
    if resp.status_code == 200:
        print "\b" + GREEN + "." + END,
        sys.stdout.flush()
    else:
        # Print colored status message to terminal
        print "\n({}) {} {}STATUS: {}{}".format(strftime("%a %b %d %Y %H:%M:%S"),
                                                SITE,
                                                YELLOW,
                                                resp.status_code,
                                                END
                                                )
        # Log status message to log file
        log = io.open('monitor.log', mode='a')
        log.write("({}) {} STATUS: {}\n".format(strftime("%a %b %d %Y %H:%M:%S"),
                                                SITE,
                                                resp.status_code,
                                                )
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
    SITES = sys.argv[1:]  # Accept sites from command line input
    email_time = {}  # Monitored sites and timestamp of last alert sent

    # Read in additional sites to monitor from sites.txt file
    try:
        SITES += [site.strip() for site in io.open('sites.txt', mode='r').readlines()]
    except IOError:
        print RED + "No sites.txt file found" + END

    # Add protocol if missing in URL
    for SITE in range(len(SITES)):
        if SITES[SITE][:7] != "http://" and SITES[SITE][:8] != "https://":
            SITES[SITE] = "http://" + SITES[SITE]

    # Eliminate exact duplicates in SITES
    SITES = list(set(SITES))

    for SITE in SITES:
        print BOLD + "Beginning monitoring of {}".format(SITE) + END
        email_time[SITE] = 0  # Initialize timestamp as 0

    while SITES:
        try:
            for SITE in SITES:
                main(SITE, email_time)
            sleep(DELAY)
        except KeyboardInterrupt:
            print RED + "\n-- Monitoring canceled --" + END
            break
    else:
        print YELLOW + "No site(s) input to monitor!" + END
