import asyncio
import threading
import Gregorian


def run_tasks_minute():
    print('Running by-minute tasks')
    server_tasks = [Gregorian.run_as_task()]
    for st in server_tasks:
        st_thread = ServerTaskThread(st)
        st_thread.start()
        while st_thread.is_alive():
            pass


def run_tasks_hour():
    print('Running by-hour tasks')
    pass


def run_tasks_day():
    print('Running by-day tasks')
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
