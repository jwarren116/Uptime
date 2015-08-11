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

When initialized, the script will output all sites to be monitored to the terminal. The script will ping each address every 60 seconds (unless otherwise configured via the `DELAY` variable found in `monitor.py`). Each ping returning a 200 status will output a green `.` to the terminal. If the address returns a status other than 200, an email will be sent using the configured SMTP settings found in `smtp_config.py` and an alert with time, address and status will be printed to the terminal. A maximum of one email per site will be sent every 30 minutes, unless otherwise configured via `EMAIL_INTERVAL` found in `monitor.py`.

## Configuring with SMS
Most mobile carriers support SMS messaging through email gateways. More information and a list of SMS Gateway Domains can be found on [wikipedia](https://en.wikipedia.org/wiki/SMS_gateway#Use_with_email_clients).
