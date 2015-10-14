
import os
import signal
import subprocess
import sys
import urllib
import urllib2

from scapy.all import *
from termcolor import colored

from date_util import *
from local_settings import MAGIC_FORM_URL
from log_file_reader import get_recent_log


currently_working = False
previous_time = None
keypress_count = None
process = None


def arp_display(pkt):
    if pkt[ARP].op == 1:
        if pkt[ARP].psrc == '0.0.0.0': # ARP Probe
            print "ARP Probe from: ", colored(pkt[ARP].hwsrc, 'blue')

            if pkt[ARP].hwsrc in ['a0:02:dc:e5:3b:d6', '74:c2:46:74:e1:8d']: # Amazon Elements, ON Nutrition
                record_event()
            else:
                print "ARP Probe from unknown device: " + pkt[ARP].hwsrc


def main_loop():
    while 1:
        print sniff(prn=arp_display, filter="arp", store=0, count=0)
        time.sleep(0.1)


def record_event():
    global currently_working, previous_time, keypress_count

    print colored('Recording the event', 'green')

    current_time = datetime.datetime.utcnow()

    time_difference = None
    task_log = None

    if currently_working:
        # Ensure that the log file has been updated, the time recorded, and keylogger stopped.
        task_log = get_recent_log()
        if not task_log:
            return

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
        'Task': task_log if currently_working else '',
    }
    currently_working = False if currently_working else True

    if keypress_count > 0:
        print 'Key presses: {key_presses}, time worked: {time}'.format(key_presses=keypress_count, time=time_difference)

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


if __name__ == '__main__':
    try:
        main_loop()
    except KeyboardInterrupt:
        print >> sys.stderr, '\nExiting by user request.\n'
        if currently_working:
            process.send_signal(signal.SIGUSR1)
            process.wait()
        sys.exit(0)
