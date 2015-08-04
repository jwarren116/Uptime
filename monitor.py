#!/usr/bin/env python
import requests
from time import sleep

SITE = "http://www.jwarren.co"

print "Beginning monitoring of {}".format(SITE)

try:
    while True:
        resp = requests.get(SITE)
        print "Status: {}".format(resp.status_code)
        sleep(5)
except KeyboardInterrupt:
    print " -- Monitoring canceled -- "
