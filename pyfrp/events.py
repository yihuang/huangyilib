'''
events
'''
from runtime import runtime
from utils import override_operaters
import operator

def liftET(func):
    def new_func(srcE, *args):
        class LiftedET(EventTransformer):
            def transform(self, value):
                return func(value, *args)
        return LiftedET(srcE)
    return new_func

def mapE(f, srcE):
    return liftET(f)(srcE)

def meta_event(name, bases, classdict):
    # wrap all operators
    for opname in override_operaters:
        classdict[opname] = liftET(getattr(operator, opname))
    return type(name, bases, classdict)

class Event(object):
    __metaclass__ = meta_event
    def __init__(self):
        self.callbacks = []
    def notify(self, value):
        for callback in self.callbacks:
            callback(value)
    def register(self, callback):
        self.callbacks.append(callback)

class EventTransformer(Event):
    def __init__(self, srcE):
        self.srcE = srcE
        super(EventTransformer,self).__init__()
        srcE.register(self.notify)
    def notify(self, value):
        value = self.transform(value)
        for callback in self.callbacks:
            callback(value)
    def transform(self, value):
        raise NotImplmented

class TimerE(Event):
    def __init__(self, period):
        self.period = period
        self.setup_timer()
        super(TimerE,self).__init__()
    def setup_timer(self):
        runtime.timer.later(self.period, self.notify)
    def notify(self, value):
        self.setup_timer()
        super(TimerE,self).notify(value)

class WithTimeE(EventTransformer):
    def transform(self, value):
        return (value, runtime.current_time)

class WithTimePeriodE(EventTransformer):
    def __init__(self, *args):
        super(WithTimePeriodE,self).__init__(*args)
        self.last_time = 0
    def transform(self, value):
        time_period = runtime.current_time-self.last_time
        result = (value, time_period)
        self.last_time = runtime.current_time
        return result

def print_(v):
    print v

def printE(e):
    e.register(print_)

