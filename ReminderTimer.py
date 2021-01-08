from threading import Thread, Event
import datetime as DT
import SQLiteInterface as SQI
class ReminderTimer(Thread):
    def __init__(self, event):
        Thread.__init__(self)
        self.stopped = event
    
    def run(self):
        while not self.stopped.wait(1):
            nowTime = DT.datetime.now()
            if(nowTime.second == 0): # Update every minute
                if SQI.reminderNow(nowTime):
                    print("Found a reminder!")
    