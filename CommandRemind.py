import LogTools as LT
import datetime as DT
import SQLiteInterface as SQI

logtag = 'CommandRemind: '

async def entry(cmdArgs, message):

    if len(cmdArgs) < 2:
        await message.channel.send('Invalid format, give at least [hh:mm time to wait] [reminder text]')
        return 
    
    # date [date] [clock time]
    if cmdArgs[0] == 'date':
        if len(cmdArgs) < 4:
            await message.channel.send('''Invalid format. Use "remind date [mm/dd/yyyy] [hh:mm] [reminder text]"''')
            return
        dateArg = cmdArgs[1]
        clocktimeArg = cmdArgs[2]
        #await remindDate(dateArg, clocktimeArg, ' '.join(cmdArgs[3:]), message)
        await createReminder('date', dateArg, clocktimeArg, ' '.join(cmdArgs[3:]), message)

    # time [clock time]
    elif cmdArgs[0] == 'time':
        if len(cmdArgs) < 3:
            await message.channel.send('''Invalid format. Use "remind time [hh:mm] [reminder text]"''')
        clocktimeArg = cmdArgs[1]
        #await remindTime(clocktimeArg, ' '.join(cmdArgs[2:]), message)
        await createReminder('clocktime', None, clocktimeArg, ' '.join(cmdArgs[2:]), message)

    # [time in hr:min]
    # Timer, runs for the amount of time given
    else:
        timeArg = cmdArgs[0]
        #await remindRaw('time', None, timeArg, ' '.join(cmdArgs[1:]), message)
        await createReminder('time', None, timeArg, ' '.join(cmdArgs[1:]), message)


async def remindDate(dateStr, clocktimeStr, text, message):
    dateInt = []
    clocktimeInt = []
    # TODO Cut/format into useable date
    # Date formats to accpet:
    # 0(0)/0(0)/00(00), 0(0)-0(0)-00(00)
    # Time formats to accept:
    # 0(0):00(am/pm)
    dateStr = dateStr.replace('/', '-')
    dateStr = dateStr.split('-')
    for s in dateStr:
        dateInt.append(int(s)) # month, day, year, in ints
    if checkDateValid(dateInt) == False:
        await message.channel.send('Invalid date format')
        return
    # Now have valid dateInt array of [m,d,y] 
    
    minFlag = ':' in clocktimeStr
    ampmFlag = ('pm' in clocktimeStr) or ('am' in clocktimeStr)
    
    if ampmFlag:
        ampm = clocktimeStr[-2:]
        clocktimeStr = clocktimeStr[:-2]
        
    clocktimeStr = clocktimeStr.split(':')
    if minFlag == False:
        clocktimeStr.append('00')

    for s in clocktimeStr:
        clocktimeInt.append(int(s)) # hour, minute
    if checkClocktimeValid(clocktimeInt, ampm) == False:
        await message.channel.send('Invalid time format')
        return
    if ampmFlag and ampm == 'pm': # Process adding 12 hours if PM is specified
        if clocktimeInt[0] == 12:
            clocktimeInt[0] = 0
        else:
            clocktimeInt[0] += 12
    # Now have valid clocktimeInt array of [h,m] CONVERTED TO MILITARY BECAUSE IM NOT DEALING WITH AMPM
    
    await createReminder(dateInt, clocktimeInt, text, message)
 
async def remindTime(clocktimeStr, text, message):
    clocktimeInt = []
    
    minFlag = ':' in clocktimeStr
    ampmFlag = ('pm' in clocktimeStr) or ('am' in clocktimeStr)
    
    if ampmFlag:
        ampm = clocktimeStr[-2:]
        clocktimeStr = clocktimeStr[:-2]
        
    clocktimeStr = clocktimeStr.split(':')
    if minFlag == False:
        clocktimeStr.append('00')

    for s in clocktimeStr:
        clocktimeInt.append(int(s)) # hour, minute
    if checkClocktimeValid(clocktimeInt, ampm) == False:
        await message.channel.send('Invalid time format')
        return
    if ampmFlag and ampm == 'pm': # Process adding 12 hours if PM is specified
        if clocktimeInt[0] == 12:
            clocktimeInt[0] = 0
        else:
            clocktimeInt[0] += 12
    # Now have valid clocktimeInt array of [h,m] CONVERTED TO MILITARY BECAUSE IM NOT DEALING WITH AMPM

async def remindRaw(timeStr, text, message):
    pass 
    
async def createReminder(rType, dateArg, timeArg, text, message):
    timeInt = []
    clocktimeInt = []
    dateInt = []
    
    if rType == 'clocktime' or rType == 'date':

        minFlag = ':' in timeArg
        ampmFlag = ('pm' in timeArg) or ('am' in timeArg)
        ampm = ''
        
        if ampmFlag:
            ampm = timeArg[-2:]
            timeArg = timeArg[:-2]
            
        timeArg = timeArg.split(':')
        if minFlag == False:
            timeArg.append('00')
    
        for s in timeArg:
            clocktimeInt.append(int(s)) # hour, minute
        if checkClocktimeValid(timeArg, ampm) == False:
            await message.channel.send('Invalid time format')
            return
        if ampmFlag and ampm == 'pm': # Process adding 12 hours if PM is specified
            if clocktimeInt[0] == 12:
                clocktimeInt[0] = 0
            else:
                clocktimeInt[0] += 12
        # Now have valid clocktimeInt array of [h,m] CONVERTED TO MILITARY BECAUSE IM NOT DEALING WITH AMPM

    if rType == 'date':

        # TODO Cut/format into useable date
        # Date formats to accpet:
        # 0(0)/0(0)/00(00), 0(0)-0(0)-00(00)
        # Time formats to accept:
        # 0(0):00(am/pm)
        dateArg = dateArg.replace('/', '-')
        dateArg = dateArg.split('-')
        for s in dateArg:
            dateInt.append(int(s)) # month, day, year, in ints
        if checkDateValid(dateInt) == False:
            await message.channel.send('Invalid date format')
            return
        # Now have valid dateInt array of [m,d,y]
    
    # Raw timer hours to add
    if rType == 'time':

        minFlag = ':' in timeArg
        
        timeArg = timeArg.split(':')
        if minFlag == False:
            timeArg.append('00')
        for s in timeArg:
            timeInt.append(int(s))
        if checkTimeValid(timeInt) == False:
            await message.channel.send('Invalid timer format')
            return
    
    fullReminder = [] # [m,d,y,h,m,text] to be created here
    
    if rType == 'time': # Add timeint to current time, get clocktime and date
        fullreminder = addTimeToNowReminder(timeInt, text)
    elif rType == 'date': # Just create the raw array from given data
        fullreminder = [dateInt[0], dateInt[1], dateInt[2], clocktimeInt[0], clocktimeInt[1], text]
    elif rType == 'clocktime': # Create from given clocktime, adding day if needed
        dtd = DT.datetime.now().date()
        fullreminder = clockTimeAdjustReminder(clocktimeInt, [dtd.month, dtd.day, dtd.year], text)
        
    SQI.addReminder(fullreminder, message.author.id)
    
def clockTimeAdjustReminder(clocktimeInt, dateInt, text):
    ret = [0,0,0,0,0,0]
    dtn = DT.datetime.now().time()
    if (dtn.hour > clocktimeInt[0]) or (dtn.hour == clocktimeInt[0] and dtn.minute >= clocktimeInt[1]):
        return addDateTimes([dateInt[0],dateInt[1],dateInt[2],clocktimeInt[0],clocktimeInt[1]],[0,1,0,0,0])
    else:
        return [dateInt[0],dateInt[1],dateInt[2],clocktimeInt[0],clocktimeInt[1],text]
    
def addArr(a1, a2):
    ret = []
    if len(a1) != len(a2):
        return None
    for i, n in enumerate(a1):
        ret.append(n + a2[i])
    return ret

def daysInMonth(m, y=0):
    if m in [1,3,5,7,8,10,12]:
        return 31
    elif m in [4,6,9,11]:
        return 30
    elif m == 2:
        if (y % 4):
            if (y % 100) and not (y % 400):
                return 28
            else:
                return 29
        else:
            return 28
    else:
        return -1

def badDate(dt):
    dinm = daysInMonth(dt[0], dt[2])
    return (dt[0] > 12) or (dt[1] > dinm) or (dt[3] >= 24) or (dt[4] >= 60)

# Adds 2 given dateTimes in the format of [m,d,y,h,m] each
def addDateTimes(dt1, dt2):
    ret = addArr(dt1, dt2)
    while badDate(ret):
        d = daysInMonth(ret[0]%12,ret[2])
        if ret[4] >= 60:
            ret[4] -= 60
            ret[3] += 1
        elif ret[3] >= 24:
            ret[3] -= 24
            ret[1] += 1
        elif ret[1] > d:
            ret[1] -= d
            ret[0] += 1
        elif ret[0] > 12:
            ret[0] -= 12
            ret[2] += 1

    return ret
  
def addTimeToNowReminder(timeInt, text):
    dt1 = [0,0,0,timeInt[0],timeInt[1]]
    dtn = DT.datetime.now().time()
    dtd = DT.datetime.now().date()
    dt2 = [dtd.month, dtd.day, dtd.year, dtn.hour, dtn.minute]
    total = addDateTimes(dt1,dt2)
    total.append(text)
    return total
      
def checkDateValid(dateIntArray):
    if len(dateIntArray) != 3:
        return False
    year = dateIntArray[2]
    day = dateIntArray[1]
    month = dateIntArray[0]
    if day < 0:
        return False
    if month in [1,3,5,7,8,10,12] and day > 31:
        return False
    if month in [4,6,9,11] and day > 30:
        return False
    if month == 2:
        if year%4 and day > 29:
            return False
        elif day > 28:
            return False
    if DT.datetime.now().date().year > year:
        return False     
    return True

def checkClocktimeValid(clocktimeIntArray, ampmStr):
    if len(clocktimeIntArray) != 2:
        return False
    hour = int(clocktimeIntArray[0])
    minute = int(clocktimeIntArray[1])
    if 'pm' in ampmStr:
        hour += 12
        if hour == 24:
            hour = 0
        elif hour > 24:
            return False
    if hour < 0 or hour > 23 or minute < 0 or minute > 59:
        return False
    
    return True

def checkTimeValid(timeIntArray):
    if len(timeIntArray) != 2:
        return False
    hour = timeIntArray[0]
    minute = timeIntArray[1]
    if hour < 0 or minute < 0 or minute > 59:
        return False
    
    return True
    

