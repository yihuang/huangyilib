from allegra import async_loop
from async_rpc import serve

class Temp(object):
    def __init__(self):
        self.remote = None
    def handle_connect(self):
        print 'connected'
    def handle_close(self):
        print 'closed'
    def say(self, str):
        print str
        self.remote.test(1)
    def test(self, a, b=1):
        print a,b

t = Temp()
serve(t, 'localhost', 9000)
async_loop.dispatch()