import time

from profiler import Timing as t


@t.timer
def include():
    time.sleep(0.1)
