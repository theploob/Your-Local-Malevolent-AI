import asyncio
import threading
import Gregorian

server_tasks_minute = []
server_tasks_hour = [Gregorian.run_as_task]
server_tasks_day = []


def run_tasks_minute():
    global server_tasks_minute
    if not __debug__:
        print('Running by-minute tasks')
    for st in server_tasks_minute:
        st_thread = ServerTaskThread(st)
        st_thread.start()
        while st_thread.is_alive():
            pass


def run_tasks_hour():
    global server_tasks_hour
    if not __debug__:
        print('Running by-hour tasks')
    for st in server_tasks_hour:
        st_thread = ServerTaskThread(st)
        st_thread.start()
        while st_thread.is_alive():
            pass


def run_tasks_day():
    global server_tasks_day
    if not __debug__:
        print('Running by-hour tasks')
    for st in server_tasks_day:
        st_thread = ServerTaskThread(st)
        st_thread.start()
        while st_thread.is_alive():
            pass


class ServerTaskThread(threading.Thread):
    def __init__(self, func):
        threading.Thread.__init__(self)
        self.func = func

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.func)
        loop.close()
