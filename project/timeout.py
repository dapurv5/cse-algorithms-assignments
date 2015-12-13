#!/usr/bin/env/python
#
# http://stackoverflow.com/questions/2281850/timeout-function-if-it-takes-too-long-to-finish
# Note: This uses signals and hence only works on UNIX. Also note how you can construct custom with's


from functools import wraps
import errno
import os
import signal

class TimeoutError(Exception):
    pass

class timeout:
    def __init__(self, seconds=1, error_message='Timeout'):
        self.seconds = seconds
        self.error_message = error_message
    def handle_timeout(self, signum, frame):
        raise TimeoutError(self.error_message)
    def __enter__(self):
        signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(self.seconds)
    def __exit__(self, type, value, traceback):
        signal.alarm(0)