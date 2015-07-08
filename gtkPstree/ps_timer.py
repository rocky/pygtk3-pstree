import threading
class TimerClass(threading.Thread):
    def __init__(self, fn, delay_in_secs=1):
        threading.Thread.__init__(self)
        self.event = threading.Event()
        self.set_delay(delay_in_secs)
        self.fn = fn

    def run(self):
        while not self.event.is_set():
            self.fn()
            self.event.wait( self.delay_in_secs )

    def stop(self):
        self.event.set()

    def set_delay(self, delay_in_secs):
        self.delay_in_secs = delay_in_secs
