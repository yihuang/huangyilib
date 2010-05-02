# coding: utf-8
from time import sleep,time
from functools import partial
from utils import Timer

class RunTime(object):
    def __init__(self):
        # behaviour update callbacks
        self.behav_callbacks = []
        self.init_time = time()
        self.current_time = 0
        self.timer = Timer()

    def run(self):
        while True:
            # update all the behaviours
            for cb in self.behav_callbacks:
                cb(self.current_time)
            # notify all the timer events
            self.timer.update(self.current_time)
            # TODO fps control
            sleep(0.1)
            self.current_time = time()-self.init_time

    def register(self, callback):
        self.behav_callbacks.append(callback)

runtime = RunTime()
