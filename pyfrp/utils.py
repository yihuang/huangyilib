import heapq
# timer implementation
class Timer(object):
    def __init__(self):
        self.timers = []

    def register(self, t, cb):
        heapq.heappush(self.timers, (t,cb))

    def later(self, t, cb):
        from runtime import runtime
        heapq.heappush(self.timers, (t+runtime.current_time,cb))

    def update(self, current_time):
        while self.timers:
            t,cb = self.timers[0]
            if t<=current_time:
                cb(current_time)
                heapq.heappop(self.timers)
            else:
                break

override_operaters = ['__lt__', '__le__', '__eq__', '__ne__', '__ge__', '__gt__', '__add__', '__and__', '__div__', '__floordiv__', '__index__', '__invert__', '__lshift__', '__mod__', '__mul__', '__neg__', '__or__', '__pos__', '__pow__', '__rshift__', '__sub__', '__truediv__', '__xor__', '__concat__', '__contains__', '__delitem__', '__delslice__', '__getitem__', '__getslice__', '__repeat__', '__setitem__', '__setslice__', '__iadd__', '__iand__', '__iconcat__', '__idiv__', '__ifloordiv__', '__ilshift__', '__imod__', '__imul__', '__ior__', '__ipow__', '__irepeat__', '__irshift__', '__isub__', '__itruediv__', '__ixor__']
