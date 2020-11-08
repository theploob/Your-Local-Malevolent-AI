# System imports
import datetime as dt
import os as os

logfile = None
logfileName = None

def Log(name, userid, chan, content):
    now = dt.datetime.now()
    
    month = now.month
    day = now.day
    hour = now.hour
    minute = now.minute
    second = now.second
    
    parts = [month, day, hour, minute, second]
    s = ['','','','','']
    i = 0
    
    for p in parts:
        if p < 10:
            s[i] = '0' + str(p)
        else:
            s[i] = str(p)
        i += 1

    timestampStr = s[0] + '/' + s[1] + ' ' + s[2] + ':' + s[3] + ':' + s[4]
    
    #print(timestampStr + '   ' + lt + m)

    # publish logs in directory ./logs/
    curDir = os.getcwd()
    logDir = curDir + '\\logs'
    os.chdir(logDir)

    global logfile
    global logfileName

    if logfileName == None:
        logfileName = 'log ' + s[0] + '_' + s[1] + '_' + s[2] + '_' + s[3] + '_' + s[4] + '.txt'
        logfile = open(logfileName, 'a', encoding='utf-8')
        logfile.write('Started log at ' + timestampStr)
        logfile.write('''\n{0} {1} {2}({3}): \t\t\t\t\t{4}'''.format(timestampStr, chan, name, str(userid), content))
        #logfile.write('\n' + timestampStr + ' ' + chan + ' ' + name + '(' + str(userid) + '): \t\t\t\t\t' + content)
        
    else:
        logfile = open(logfileName, 'a', encoding='utf-8')
        logfile.write('''\n{0} {1} {2}({3}): \t\t\t\t\t{4}'''.format(timestampStr, chan, name, str(userid), content))
        #logfile.write('\n' + timestampStr + ' ' + chan + ' ' + name + '(' + str(userid) + '): \t\t\t\t\t' + content)
    
    logfile.close()
    
    os.chdir(curDir)
