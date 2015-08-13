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
COLOR_DICT = {
    "green": "\033[92m",
    "red": "\033[91m",
    "yellow": "\033[93m",
    "bold": "\033[1m",
    "end": "\033[0m",
    }

# Message template for alert
message = """From: {sender}
To: {receivers}
Subject: Monitor Service Notification

You are being notified that {site} is experiencing a {status} status!
"""


def colorize(text, color):
    # print COLOR_DICT
    return COLOR_DICT[color] + str(text) + COLOR_DICT['end']


def ping(site, last_email_time):
    resp = requests.get(site)
    if resp.status_code == 200:
        print "\b" + colorize(".", "green"),
        sys.stdout.flush()
    else:
        # Print colored status message to terminal
        print "\n({}) {} STATUS: {}".format(strftime("%a %b %d %Y %H:%M:%S"),
                                            site,
                                            colorize(resp.status_code, "yellow"),
                                            )
        # Log status message to log file
        log = io.open('monitor.log', mode='a')
        log.write("({}) {} STATUS: {}\n".format(strftime("%a %b %d %Y %H:%M:%S"),
                                                site,
                                                resp.status_code,
                                                )
                  )
        # If more than EMAIL_INTERVAL seconds since last email, resend
        if (time() - last_email_time[site]) > EMAIL_INTERVAL:
            try:
                smtpObj = smtplib.SMTP(host, port)  # Set up SMTP object
                smtpObj.starttls()
                smtpObj.login(sender, password)
                smtpObj.sendmail(sender,
                                 receivers,
                                 message.format(sender=sender,
                                                receivers=", ".join(receivers),
                                                site=site,
                                                status=resp.status_code
                                                )
                                 )
                last_email_time[site] = time()  # Update time of last email
                print colorize("Successfully sent email", "green")
            except smtplib.SMTPException:
                print colorize("Error sending email ({}:{})".format(host, port), "red")


def main():
    SITES = sys.argv[1:]  # Accept sites from command line input
    last_email_time = {}  # Monitored sites and timestamp of last alert sent

    # Read in additional sites to monitor from sites.txt file
    try:
        SITES += [site.strip() for site in io.open('sites.txt', mode='r').readlines()]
    except IOError:
        print colorize("No sites.txt file found", "red")

    # Add protocol if missing in URL
    for site in range(len(SITES)):
        if SITES[site][:7] != "http://" and SITES[site][:8] != "https://":
            SITES[site] = "http://" + SITES[site]

    # Eliminate exact duplicates in SITES
    SITES = list(set(SITES))

    for site in SITES:
        print colorize("Beginning monitoring of {}".format(site), "bold")
        last_email_time[site] = 0  # Initialize timestamp as 0

    while SITES:
        try:
            for site in SITES:
                ping(site, last_email_time)
            sleep(DELAY)
        except KeyboardInterrupt:
            print colorize("\n-- Monitoring canceled --", "red")
            break
    else:
        print colorize("No site(s) input to monitor!", "red")


if __name__ == '__main__':
    main()
