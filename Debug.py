from CommandRemind import addArr
from CommandRemind import addDateTimes
from threading import Timer
from threading import Event
import ReminderTimer
import time


def expect(func, result, tag):
    try:
        ret = (func == result)
    except Exception as e:
        print('''Exception encountered''')
        print(e)
        return None
    if ret:
        return ret
    else:
        print("Error in {0}: Expected {1}, got {2}".format(tag, result, func))
        return ret

tests = [
    expect(addDateTimes([1,1,2020,0,0],[1,1,1,1,1]),[2,2,2021,1,1],"addDateTimes"),
    expect(addDateTimes([1,1,2020,23,50],[0,0,0,0,15]),[1,2,2020,0,5],"addDateTimes"),
    expect(addDateTimes([12,20,2019,0,0],[1,53,0,0,0]),[3,13,2020,0,0],"addDateTimes"),
    expect(addDateTimes([12,20,2020,0,0],[1,53,0,0,0]),[3,14,2021,0,0],"addDateTimes"),
    expect(addDateTimes([12,20,2020,0,0],[1,53,0,0,0]),[3,14,2021,0,0],"addDateTimes"),
    
    expect(addArr([1,2,3],[1,1,1]),[2,3,4],"addArr"),
    expect(addArr([1,2,3],[1,1]),None,"addArr"),
    expect(addArr([],[]),[],"addArr")
]

def debug():
    print(CommandRemind.daysInMonth(1))

def testListRun():   
    for i, t in enumerate(tests):
        if t == False:
            print("Test {0} failed".format(i))

if __name__ == "__main__":
    testListRun()
    stopFlag = Event()
    thread = ReminderTimer.ReminderTimer(stopFlag)
    thread.start()
    time.sleep(5)
    stopFlag.set()
