#!/usr/bin/env python

from sdog import SDNotifier
import time

sd = SDNotifier()
sd.ready()

while True:
    sd.status("I am alive at %s" % time.time())
    sd.watchdog()
    time.sleep(1)
