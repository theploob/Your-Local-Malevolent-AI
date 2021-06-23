import SQLiteInterface as SQI
import re
import datetime

logtag = 'CommandRemind: '

async def entry(cmdArgs, message):

    if len(cmdArgs) < 2:
        await message.channel.send('Invalid format, give at least [hh:mm time to wait] [reminder text]')
        return 

    valid_ret = validate_command(cmdArgs)
    if valid_ret[0]:
        pass
    else:
        print(valid_ret[1])

    # date [date] [clock time]
    # eg >remind date 09/15/2021 15:30 smack Sam
    # the reminder will go out on 9/15/2021 at 15:30

    # time [clock time]
    # eg >remind 15:30 smack Sam
    # the next time 15:30 rolls around the reminder will go out

    # [time in hr:min]
    # eg >remind 4:30 smack Sam
    # Timer, runs for the amount of time given


def validate_command(args):
    cmd_type = args[0]
    cmd_args = args[1:]
    date_err = '''Invalid format. Use "remind date [mm/dd/yyyy] [hh:mm] [reminder text]"'''
    time_err = '''Invalid format. Use "remind time [hh:mm] [reminder text]"'''

    if cmd_type == 'date':
        if len(cmd_args) < 3:
            return [False, date_err]
        date_arg_str = cmd_args[0]
        time_arg_str = cmd_args[1]
        msg_arg = cmd_args[2]

        date_arg = split_date_arg(date_arg_str)
        if date_arg[3]:
            return [False, date_err]
        if not is_valid_date(date_arg):
            return [False, date_err]

        time_arg = split_time_arg(time_arg_str)
        if time_arg[2]:
            return [False, date_err]
        if not is_valid_time(time_arg):
            return [False, date_err]

        # Set the reminder
        return [True, create_reminder(date_arg[:-1] + time_arg[:-1], msg_arg)]

    elif cmd_type == 'time':
        if len(cmd_args) < 2:
            return [False, time_err]
        time_arg_str = cmd_args[0]
        msg_arg = cmd_args[1]

        time_arg = split_time_arg(time_arg_str)
        if time_arg[2]:
            return [False, time_err]
        if not is_valid_time(time_arg):
            return [False, time_err]

        ct = datetime.datetime.now()
        current_datetime = [ct.month, ct.day, ct.year, ct.hour, ct.minute]

        if time_is_after(time_arg[:-1], [ct.hour, ct.minute]):
            return [True, create_reminder(current_datetime[0:3] + time_arg[:-1], msg_arg)]
        else:
            new_date = add_date_args(current_datetime[0:3], [0, 1, 0])
            return [True, create_reminder(new_date + time_arg[:-1], msg_arg)]

    else:  # No command type, just set a timer for the given duration
        pass


# Takes datetime styled argument - [month, day, year, hour, minute] and the msg_arg
def create_reminder(datetime_arg, msg_arg):
    pass


# Adds date_args together, returns the total date_arg
# The second date arg is added literally, and is not interpreted as an actual date
def add_date_args(a, b):
    ret_arg = a
    ret_arg[0] += b[0]
    ret_arg[1] += b[1]
    ret_arg[2] += b[2]

    # Correct days/months
    valid = False
    while not valid:
        if ret_arg[0] in [1, 3, 5, 7, 8, 10, 12]:
            if ret_arg[1] > 31:
                ret_arg[1] -= 31
                ret_arg[0] += 1
            else:
                valid = True
        elif ret_arg[0] in [4, 6, 9, 11]:
            if ret_arg[1] > 30:
                ret_arg[1] -= 30
                ret_arg[0] += 1
            else:
                valid = True
        else:
            if is_leap_year(ret_arg[2]):
                if ret_arg[1] > 29:
                    ret_arg[1] -= 29
                    ret_arg[0] += 1
                else:
                    valid = True
            else:
                if ret_arg[1] > 28:
                    ret_arg[1] -= 28
                    ret_arg[0] += 1
                else:
                    valid = True

    # Correct months/years
    while ret_arg[0] > 12:
        ret_arg[2] += 1
        ret_arg[0] -= 12
    while ret_arg[0] < 1:
        ret_arg[2] -= 1
        ret_arg[0] += 12

    return ret_arg


# Takes 2 time_args and returns if the first is after the second
def time_is_after(a, b):
    if a[0] == b[0]:
        return a[1] > b[1]
    return a[0] > b[0]


# Splits the given time string into 2 parts, all ints
# Returns [h, m, err] - h, m are 0 when err == True
def split_time_arg(arg):
    split_arg = re.split(':', arg)
    if len(split_arg) != 2:
        return [0, 0, True]
    else:
        return [int(split_arg[0]), int(split_arg[1]), False]


# Splits the given date string into 3 parts, all ints
# Returns [m, d, y, err] - m, d, and y are 0 when err == True
def split_date_arg(arg):
    split_arg = re.split('/|-', arg)
    if len(split_arg) != 3:
        return [0, 0, 0, True]
    else:
        return [int(split_arg[0]), int(split_arg[1]), int(split_arg[2]), False]


# Check that the given time, in int format, is a valid time
def is_valid_time(v):
    h = v[0]
    m = v[0]
    if h > 23 or h < 0:
        return False
    if m > 59 or m < 0:
        return False
    return True


# Check that the given date, in int format, is a valid date
def is_valid_date(v):
    m = v[0]
    d = v[1]
    y = v[2]
    if m > 12 or m < 1:
        return False
    if d < 1:
        return False
    if m in [1, 3, 5, 7, 8, 10, 12]:
        return d <= 31
    elif m in [4, 6, 9, 11]:
        return d <= 30
    else:
        if is_leap_year(y):
            return d <= 29
        else:
            return d <= 28


def is_leap_year(y):
    if y % 2000:
        return False
    return y % 4 == 0
