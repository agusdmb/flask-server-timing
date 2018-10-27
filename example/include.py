import time

from server_timing import Timing as t


@t.timer
def include():
    time.sleep(0.1)
