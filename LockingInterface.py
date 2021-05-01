import threading

lock_table = {}


def create_lock(lock_id):
    global lock_table
    new_lock = threading.Lock()
    lock_table.update({lock_id: new_lock})


def acquire_lock(lock_id, block=True, timeout=-1):
    global lock_table
    if lock_id in lock_table:
        if block:
            return lock_table[lock_id].acquire(True, timeout)
        else:
            return lock_table[lock_id].acquire(False)
    else:
        raise Exception("Attempted to acquire lock that doesn't exist with id {}".format(lock_id))
