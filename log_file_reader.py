import os
import subprocess
import sys
import time

from termcolor import colored


log_last_modified = None


def get_recent_log():
    global log_last_modified

    filename = 'log.txt'

    try:
        new_last_modified = os.path.getmtime(filename)
    except OSError, e:
        print colored('ERROR!', 'red', attrs=['bold', 'blink'])
        print colored('File not found, expected \'log.txt\' in current directory', 'red')
        return

    if new_last_modified == log_last_modified:
        print colored('ERROR!', 'red', attrs=['bold', 'blink'])
        print colored('The log file has not been updated', 'red')
        return ''

    log_last_modified = new_last_modified

    with open(filename, 'r') as log:
        return log.read()
