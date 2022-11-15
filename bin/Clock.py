import os
import random
import time
from . import Settings
from .Sender import ActiveSender
from threading import Thread

# ---------------------------------------------------------------------------
# Clock Class
# ---------------------------------------------------------------------------

class LogicalClock (Thread):
    # init method
    def __init__(self, data):
        # initializes the clock
        Thread.__init__(self)
        self.params = Settings.CLOCK_PARAMS
        self.MASTER_IP = Settings.MASTER_IP
        self.clear_type = Settings.CLEAR_TYPE
        self.data = data
        self.second = 0
        self.minute = 0
        self.hour = 0

    # timePass method
    def timePass(self):
        # advance the clock's time in 1 sec
        time.sleep(1)
        self.second += 1
        if self.second == 60:
            self.second = 0
            self.minute += 1
            if self.minute == 60:
                self.minute = 0
                self.hour += 1
                if self.hour == 24:
                    self.hour = 0
        current_time = self.getTime()
        print("%02d:%02d:%02d" % (
            current_time['HOUR'],
            current_time['MINUTE'],
            current_time['SECOND']))

    # syncronize_time method
    def syncronize_time(self):
        # synchronize the clocks
        os.system(self.clear_type)
        print('Starting Sync...')
        send = ActiveSender(self.getTime(), self.MASTER_IP, 61667)
        send.start()
        send.join()
        while(True):
            json = self.data.getJson()
            if json != 'NULL':
                self.setTime(json)
                break
        print("Sync Success! New Time: %02d:%02d:%02d" % (
            json['HOUR'],
            json['MINUTE'],
            json['SECOND']))

    # fakeTimePass method
    def realTimePass(self):
        # pass the clock's time
        sync_count = 0
        while(True):
            sync_count += 1
            self.timePass()
            if sync_count == self.params['SYNC_INTERVAL']:
                sync_count = 0
                self.syncronize_time()

    # fakeTimePass method
    def fakeTimePass(self):
        # pass the clock's time in an unbalanced way
        confusion_count = 0
        sync_count = 0
        while(True):
            confusion_count += 1
            sync_count += 1
            self.timePass()
            if sync_count == self.params['SYNC_INTERVAL']:
                sync_count = 0
                self.syncronize_time()
            if confusion_count == self.params['CONFUSION_INTERVAL']:
                confusion_count = 0
                confusion = random.randint(
                    -self.params['CONFUSION_RANGE'], self.params['CONFUSION_RANGE'])
                self.second = self.second + confusion

    # getTime method
    def getTime(self):
        # return the current clock's time
        time_dict = {'HOUR': self.hour,
                     'MINUTE': self.minute,
                     'SECOND': self.second}
        return time_dict

    # setTime method
    def setTime(self, json):
        # sets the current clock time
        self.hour = json['HOUR']
        self.minute = json['MINUTE']
        self.second = json['SECOND']

    # run method
    def run(self):
        # start the clock thread
        if self.params['MODE'] == 'REAL':
            self.realTimePass()
        elif self.params['MODE'] == 'FAKE':
            self.fakeTimePass()
        else:
            print('Clock MODE Error')
