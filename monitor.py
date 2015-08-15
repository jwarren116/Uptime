#!/usr/bin/env python

"""A simple Python script for monitoring the status of one or more websites

Command line usage: python monitor.py http://www.example.com

Set Up
The monitor.py script is configured to send alert emails when a non-200 status
is encountered. Settings for emailing must be configured in the
smtp_config.py module. Settings are as follows:

- sender: the email address/login address for the website service sending the
alerts (ex: john.smith@gmail.com)
- password: the password for the email service sending the alert
- host: the host that verifies your SMTP credentials (ex: mail.example.com
or smtp.gmail.com)
- port: SMTP port (typically 587, 25, or 465)
- receivers: the list of recipients receiving the alert

Running
The monitor.py script runs from the command line, optionally taking one or more
websites as arguments(ex: python monitor.py http://www.github.com
http://www.google.com). The script then reads in the optional sites.txt file
containing additional sites (one per line).

When initialized, the script will output all sites to be monitored to the
terminal. The script will ping each address every 60 seconds (unless otherwise
configured via the DELAY variable found in monitor.py). Each ping returning
a 200 status will output a green `.` to the terminal. If the address returns a
status other than 200, an email will be sent using the configured SMTP settings
found in smtp_config.py and an alert with time, address and status will be
printed to the terminal. A maximum of one email per site will be sent every 30
minutes, unless otherwise configured via EMAIL_INTERVAL found
in monitor.py.

Configuring with SMS
Most mobile carriers support SMS messaging through email gateways. More
information and a list of SMS Gateway Domains can be found at
https://en.wikipedia.org/wiki/SMS_gateway#Use_with_email_clients.
"""

from __future__ import unicode_literals
from time import sleep, time, strftime
import requests
import io
import smtplib
import sys
from smtp_config import sender, password, receivers, host, port


DELAY = 60  # Delay between site queries
EMAIL_INTERVAL = 1800  # Delay between alert emails

last_email_time = {}  # Monitored sites and timestamp of last alert sent

# Define escape sequences for colored terminal output
COLOR_DICT = {
    "green": "\033[92m",
    "red": "\033[91m",
    "yellow": "\033[93m",
    "bold": "\033[1m",
    "end": "\033[0m",
    }

# Message template for alert
MESSAGE = """From: {sender}
To: {receivers}
Subject: Monitor Service Notification

You are being notified that {site} is experiencing a {status} status!
"""


def colorize(text, color):
    """Return input text wrapped in ANSI color codes for input color."""
    return COLOR_DICT[color] + str(text) + COLOR_DICT['end']


def error_log(site, status_code):
    """Log errors to stdout and log file, and send alert email via SMTP."""
    # Print colored status message to terminal
    print "\n({}) {} STATUS: {}".format(strftime("%a %b %d %Y %H:%M:%S"),
                                        site,
                                        colorize(status_code, "yellow"),
                                        )
    # Log status message to log file
    with open('monitor.log', 'a') as log:
        log.write("({}) {} STATUS: {}\n".format(strftime("%a %b %d %Y %H:%M:%S"),
                                                site,
                                                status_code,
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
                             MESSAGE.format(sender=sender,
                                            receivers=", ".join(receivers),
                                            site=site,
                                            status=status_code
                                            )
                             )
            last_email_time[site] = time()  # Update time of last email
            print colorize("Successfully sent email", "green")
        except smtplib.SMTPException:
            print colorize("Error sending email ({}:{})".format(host, port), "red")


def ping(site):
    """Send GET request to input site

    A 200 response status results in a green '.' printed to stdout
    A non-200 response status results in a call to error_log(), passing site
    and the response status
    """
    resp = requests.get(site)
    if resp.status_code == 200:
        print "\b" + colorize(".", "green"),
        sys.stdout.flush()
    else:
        error_log(site, resp.status_code)


def get_sites():
    """Return list of unique URLs from input and sites.txt file."""
    sites = sys.argv[1:]  # Accept sites from command line input

    # Read in additional sites to monitor from sites.txt file
    try:
        sites += [site.strip() for site in io.open('sites.txt', mode='r').readlines()]
    except IOError:
        print colorize("No sites.txt file found", "red")

    # Add protocol if missing in URL
    for site in range(len(sites)):
        if sites[site][:7] != "http://" and sites[site][:8] != "https://":
            sites[site] = "http://" + sites[site]

    # Eliminate exact duplicates in sites
    sites = list(set(sites))

    return sites


def main():
    sites = get_sites()

    for site in sites:
        print colorize("Beginning monitoring of {}".format(site), "bold")
        last_email_time[site] = 0  # Initialize timestamp as 0

    while sites:
        try:
            for site in sites:
                ping(site)
            sleep(DELAY)
        except KeyboardInterrupt:
            print colorize("\n-- Monitoring canceled --", "red")
            break
    else:
        print colorize("No site(s) input to monitor!", "red")


if __name__ == '__main__':
    main()
