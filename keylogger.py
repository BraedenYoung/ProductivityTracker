import signal
import subprocess
import sys
import time

from AppKit import NSApp
from AppKit import NSApplication
from Foundation import NSLog
from Foundation import NSObject
from Cocoa import NSEvent
from Cocoa import NSKeyDownMask
from PyObjCTools import AppHelper


counter = 0


class AppDelegate(NSObject):
    def applicationDidFinishLaunching_(self, notification):
        mask = NSKeyDownMask
        NSEvent.addGlobalMonitorForEventsMatchingMask_handler_(mask, handler)


def handler(event):
    global counter
    counter += 1


def main():
    app = NSApplication.sharedApplication()
    delegate = AppDelegate.alloc().init()
    NSApp().setDelegate_(delegate)
    AppHelper.runEventLoop()


def return_counter_and_quit(*args):
    sys.stdout.write('{keypress_count}'.format(keypress_count=counter))
    AppHelper.stopEventLoop()
    exit()


if __name__ == '__main__':

    signal.signal(signal.SIGUSR1, return_counter_and_quit)

    try:
        main()
    except KeyboardInterrupt:
        print >> sys.stderr, '\nExiting by user request.\n'
        exit(0)
