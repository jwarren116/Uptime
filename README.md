# Uptime
### A simple Python script for monitoring the status of one or more websites.

## Set Up
The monitor.py script is configured to send alert emails when a non-200 status is encountered. Settings for emailing must be configured in the `smtp_config.py` module. Settings are as follows:

- `sender`: the email address/login address for the website service sending the alerts (ex: `john.smith@gmail.com`)
- `password`: the password for the email service sending the alert
- `host`: the host that verifies your SMTP credentials (ex: `mail.example.com` or `smtp.gmail.com`)
- `port`: SMTP port (typically 587, 25, or 465)
- `receivers`: the list of recipients receiving the alert

## Running
The monitor.py script runs from the command line, optionally taking one or more websites as arguments(ex: `python monitor.py http://www.github.com http://www.google.com`). The script then reads in the optional `sites.txt` file containing additional sites (one per line).
