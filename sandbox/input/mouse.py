#!/usr/bin/python

from pymouse import PyMouseEvent
import time

class DetectMouseClick(PyMouseEvent):
    def __init__(self):
        PyMouseEvent.__init__(self)

    def click(self, x, y, button, press):
        if button == 1:
            if press:
                print("x="+str(x)+";y="+str(y))
                self.stop()
            else:
                print("end")
        else:
            self.stop()

O = DetectMouseClick()
O.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    O.stop()

