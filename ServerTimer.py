import time
import ServerTimerTasks

last_checked_time = None
stop_flag = False


def start_timer(thread_name):
    global last_checked_time
    current_time_s = time.time()
    current_time_struct = time.localtime(current_time_s)
    last_checked_time = current_time_struct
    while not stop_flag:
        current_time_struct = time.localtime(time.time())
        if is_next_minute(current_time_struct, last_checked_time):
            ServerTimerTasks.run_tasks_minute()
        if is_next_hour(current_time_struct, last_checked_time):
            ServerTimerTasks.run_tasks_hour()
        if is_next_day(current_time_struct, last_checked_time):
            ServerTimerTasks.run_tasks_day()
        last_checked_time = current_time_struct
        time.sleep(60)
    print("Timer stop flag was triggered: stopping start_timer()")
    thread_name.exit()


def stop_timer():
    global stop_flag
    stop_flag = True


def is_next_minute(current, last):
    if current.tm_min > last.tm_min:
        return True
    if current.tm_hour > last.tm_hour:
        return True
    if current.tm_mday > last.tm_mday:
        return True
    if current.tm_mon > last.tm_mon:
        return True
    if current.tm_year > last.tm_year:
        return True
    return False


def is_next_hour(current, last):
    if current.tm_hour > last.tm_hour:
        return True
    if current.tm_mday > last.tm_mday:
        return True
    if current.tm_mon > last.tm_mon:
        return True
    if current.tm_year > last.tm_year:
        return True
    return False


def is_next_day(current, last):
    if current.tm_mday > last.tm_mday:
        return True
    if current.tm_mon > last.tm_mon:
        return True
    if current.tm_year > last.tm_year:
        return True
    return False
