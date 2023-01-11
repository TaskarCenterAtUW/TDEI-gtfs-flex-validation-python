from time import sleep
from threading import Timer
from .validation import Validation



class Monitor(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.start()
        self.messages = []

    def _run(self):
        self.is_running = False
        self.start()
        self.messages = self.function(**self.kwargs)
        self.validate_message(message=self.messages)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False

    def validate_message(self, message=[]):
        Validation(message=message)
