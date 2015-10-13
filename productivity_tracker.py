
import datetime
import os
import signal
import subprocess
import sys
import time
import urllib
import urllib2

from dateutil import tz
from scapy.all import *


MAGIC_FORM_URL = 'http://api.cloudstitch.com/braedenyoung/magic-form-2/datasources/sheet'


currently_working = False
previous_time = None
keypress_count = None
process = None


def arp_display(pkt):
    if pkt[ARP].op == 1: #who-has (request)
        if pkt[ARP].psrc == '0.0.0.0': # ARP Probe
            print "ARP Probe from: " + pkt[ARP].hwsrc

            if pkt[ARP].hwsrc == 'a0:02:dc:e5:3b:d6': # Amazon Elements
                print "Pressed!"
                record_event()
            else:
                print "ARP Probe from unknown device: " + pkt[ARP].hwsrc


def main_loop():
    while 1:
        print sniff(prn=arp_display, filter="arp", store=0, count=0)
        time.sleep(0.1)


def record_event():
    global currently_working, previous_time, keypress_count

    print 'Recording the event'

    current_time = datetime.datetime.utcnow()

    time_difference = ''

    if currently_working:
        time_difference = get_time_delta(current_time, previous_time)
        keypress_count = stop_keylogger()

    else:
        start_keylogger()
        keypress_count = 0
        previous_time = current_time

    data = {
        'Date': format_and_localize_time(current_time),
        'Event': 'Started Working' if not currently_working else 'Finished working',
        'Number of Keypresses': keypress_count,
        'Time Worked': time_difference,
    }
    currently_working = False if currently_working else True

    response = urllib2.urlopen(MAGIC_FORM_URL, data=urllib.urlencode(data))


def start_keylogger():
    global process
    cmd = ["sudo", "python", "keylogger.py"]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def stop_keylogger():
    process.send_signal(signal.SIGUSR1)
    process.wait()

    result = process.stdout.read()

    return result


def get_time_delta(current, previous):
    return strfdelta((current - previous),
    '{minutes}') if previous else ''


def format_and_localize_time(time_value):
    time_value = time_value.replace(tzinfo=tz.tzutc())
    localized_time = time_value.astimezone(tz.tzlocal())

    return localized_time.strftime("%Y-%m-%d %H:%M:%S")


def strfdelta(tdelta, fmt):
    d = {"days": tdelta.days}
    d["hours"], rem = divmod(tdelta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    return fmt.format(**d)


if __name__ == '__main__':
    try:
        main_loop()
    except KeyboardInterrupt:
        print >> sys.stderr, '\nExiting by user request.\n'
        sys.exit(0)
