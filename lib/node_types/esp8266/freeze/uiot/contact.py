# Contact Device
# author: ulno
# created: 2017-04-08

from machine import Pin
from uiot.device import Device


####### simple Input, contact devices/push buttons
class Contact(Device):
    # Handle contact or button like devices
    def __init__(self, name, pin, *args,
                 report_high="on", report_low="off",
                 pullup=True, threshold=0,
                 on_change=None, report_change=True, filter=None):
        if len(args) > 0:
            report_high = args[0]
            if len(args) > 1:
                report_low = args[1]
        Device.__init__(self, name, pin,
                        value_map={True: report_high,
                                   False: report_low},
                        on_change=on_change,
                        report_change=report_change, filter=filter)
        if pullup:
            pin.init(Pin.IN, Pin.PULL_UP)
        else:
            pin.init(Pin.IN)
            try:
                Pin.init(Pin.OPEN_DRAIN)
            except:
                pass
        self.threshold = threshold + 1
        self.debouncer = self.port() * self.threshold

    def measure(self):
        if self.port() == 1:
            self.debouncer += 1
            if self.debouncer > self.threshold * 2 - 1:
                self.debouncer = self.threshold * 2 - 1
        else:
            self.debouncer -= 1
            if self.debouncer < 0:
                self.debouncer = 0
        return self.debouncer >= self.threshold
