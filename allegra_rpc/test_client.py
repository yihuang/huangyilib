from allegra import async_loop
from async_rpc import connect

class Temp(object):
    def handle_connect(self):
        print 'connected'
    def handle_close(self):
        print 'closed'
    def say(self, str):
        print str
        self.remote.say(str)
    def test(self, a, b=1):
        print a,b

t = Temp()
connect(t, 'localhost', 9000)
t.say('hello')
t.remote.test(1,2)
async_loop.dispatch()