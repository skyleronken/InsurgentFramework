import threading

#
#This module is added for the sake of simplifying the interaction of threads running within the bot.
#Should make it easier to manage the implementation of threading command modules.
#

THREAD_KEY = 't_ref'

threads = {}

class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self, target, args):
        super(StoppableThread, self).__init__()
        self._stop = threading.Event()
        self.target = target
        self.args = args

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()
        
    def run(self):
        try:
            self.args[THREAD_KEY] = self
            self.target(self.args)
        except Exception, e:
            return e

def run_in_thread(func, args=None):
    if not hasattr(func, '__call__'):
        return None
    else:
        try:
            t = StoppableThread(func, args)
            t.setDaemon(True)
            t.start()
            threads[t.getName()] = t
            return True, t.getName()
        except Exception, e:
            return False, e

def list_threads():
    # main_thread = threading.currentThread()
    # thread_list = []
    # for t in threading.enumerate():
    #     if t is main_thread:
    #         continue
    #     thread_list.append(t.getName())
    # return thread_list
    return list(threads.keys())
    
def stop_thread(name):
    t = threads[name]
    t.stop()

def set_thread_name(old_name, new_name):
    t = threads[old_name]
    del threads[old_name]
    threads[new_name] = t