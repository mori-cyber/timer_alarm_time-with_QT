import sys
import os

import time
from PySide6.QtWidgets import *
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
# from threading import Thread
from PySide6.QtCore import QThread
from playsound import playsound
from datetime import datetime
from functools import partial
from win10toast import ToastNotifier

# -----------------------------------------------
#                   stopwatch
# ------------------------------------------------
class Timer(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.h = 0
        self.m = 0
        self.s = 0
    def reset(self):
        self.h = 0
        self.m = 0
        self.s = 0
    def increase(self):
        self.s+=1
        if self.s>=60:
            self.s = 0
            self.m+=1
        if self.m>=60:
            self.m=0
            self.h+=1
    def run(self):
        while True:
            self.increase()
            window.ui.lbl_stopwatch.setText(f"{self.h}:{self.m}:{self.s}")
            time.sleep(1)

class Timmer(QWidget):
    def __init__(self):
        super(Timmer, self).__init__()
        loader = QUiLoader()
        self.ui = loader.load("form.ui")
        self.ui.btn_stopwhatch_start.clicked.connect(self.starstoptwatch)
        self.ui.btn_stopwatchpuse.clicked.connect(self.pausestopwatch)
        self.ui.btn_stopwatchstop.clicked.connect(self.stopstartwatch)
        self.ui.btn_REC.clicked.connect(self.record)
        # alarm_
        self.ui.btn_Do_Alarm.clicked.connect(self.doAlarm)
        # timer
        self.ui.btn_start.clicked.connect(self.start)
        self.ui.btn_pause.clicked.connect(self.pause)
        self.ui.btn_stop.clicked.connect(self.stop)
        self.timer = Timer()
        self.ui.show()
    # ------------------------------------------------------------
    #                        ALARM
    # ------------------------------------------------------------
    def doAlarm(self):
        self.alarm = Alarm()
        self.alarm.start()



    def record(self):
        label = QLabel()
        label.setText(self.ui.lbl_watch.text())
        self.ui.GL.addWidget(label)


    def pausestopwatch(self):
        self.timer.terminate()
    def stopstartwatch(self):
        self.timer.terminate()
        self.timer.reset()
        self.ui.lbl_stopwatch.setText("00:00:00")

    def starstoptwatch(self):

        self.timer.start()
    # ----------------------------------------------------------
    #                      TIMER
    # __________________________________________________________
    def pause(self):
        self.cornometer.terminate()

    def stop(self):
        self.cornometer.terminate()
        self.cornometer.reset()
        self.ui.label_STOP.setText("00:00:00")

    def start(self):
        self.cornometer = Cornometer(self.ui.SB_1.value(),
                             self.ui.SB_2.value(),
                             self.ui.SB_3.value())
        self.cornometer.start()

class Alarm(QThread):
        def __init__(self):
            QThread.__init__(self)
            self.hour = window.ui.SB_h.value()
            self.minute = window.ui.SB_m.value()
            self.toast = ToastNotifier()

        def run(self):
            while True:
                this_time = datetime.now()
                now_one = this_time.strftime("%H:%M:%5")
                time_now = now_one.split(':')
                if self.hour == int(time_now[0]) and self.minute == int(time_now[1]):
                    self.toast.show_toast( "Timer ", "biiiiip alarm", "duration=10")
                    playsound("1.mp3")

                time.sleep(1)


class Cornometer(QThread):
    def __init__(self, h, m, s):
        QThread.__init__(self)
        self.st = h
        self.mt = m
        self.ht = s

    def reset(self):
        self.st = 0
        self.mt = 0
        self.ht = 0

    def decrease(self):

        if self.ht == 0 and self.mt == 0 and self.st == 0:
            return

        if self.st == 0 and self.mt > 0:
            self.st = 59
            self.mt -= 1

        if self.mt == 0 and self.ht > 0:
            self.mt = 59
            self.ht -= 1

        self.st -= 1

if __name__ == "__main__":
    app = QApplication([])
    window = Timmer()
    sys.exit(app.exec_())
