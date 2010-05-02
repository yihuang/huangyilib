'''
behaviours
'''
from runtime import runtime
import operator
from functools import partial
from utils import override_operaters

# lift normal function to hehavious function
def liftB(func):
    def new_func(*args):
        def impl(self, time):
            return func(*(isinstance(b, Behaviour) and b(time) or b for b in args))
        return new_behaviour(impl)()
    return new_func

def meta_behaviour(name, bases, classdict):
    # wrap all operators
    for opname in override_operaters:
        classdict[opname] = liftB(getattr(operator, opname))
    return type(name, bases, classdict)

# behaviours
class Behaviour(object):
    __metaclass__ = meta_behaviour
    __valtype__ = None
    def __call__(self,time):
        raise NotImplmented

def new_behaviour(impl):
    class NewBehaviour(Behaviour):
        __call__ = impl
    return NewBehaviour

# convert event to behavious
class StartsWithB(Behaviour):
    def __init__(self, sourceE, initialVal):
        self.__class__.__valtype__ = type(initialVal)
        self.value = initialVal
        sourceE.register(self.notify)

    def notify(self, value):
        self.value = value

    def __call__(self, time):
        return self.value

TimeB = new_behaviour(lambda o,t:t)()

def TimerB(period):
    from events import TimerE
    return StartsWithB(TimerE(period), runtime.current_time)

def print_b(b, v):
    print b(v)

def printB(b):
    runtime.register(partial(print_b, b))


