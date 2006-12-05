import pickle
from allegra import (
        async_loop, async_chat,
        async_server, async_client )

def dump_call(funcname, args, kwargs):
    para = (args, kwargs)
    para = pickle.dumps( para )
    data = funcname + '\t' + para
    length = len(data)
    return '%s\r\n%s' % ( hex(length), data )

def parse_call(data):
    funcname, para = data.split('\t', 1)
    para = pickle.loads(para)
    return funcname, para

class Dispatcher(async_chat.Dispatcher):
    ''' the dispatcher for both server and client '''
    terminator = '\r\n'
    def __init__(self, obj):
        super(Dispatcher, self).__init__()
        self.buffer = []
        self.obj = obj
        self.obj.remote = Remote(self.async_chat_push)

    def handle_connect(self):
        self.obj.handle_connect()

    def handle_close(self):
        self.close()
        self.obj.handle_close()

    def collect_incoming_data(self, data):
        self.buffer.append(data)

    def found_terminator(self):
        data = ''.join(self.buffer)
        self.buffer = []
        if not data:
            return True
        if self.terminator == '\r\n':
            length = int(data, 16)
            self.set_terminator(length)
        else:
            self.set_terminator('\r\n')
            self.call(data)

    def call(self, data):
        funcname, para = parse_call(data)
        try:
            func = getattr(self.obj, funcname)
        except AttributeError:
            return
        else:
            try:
                func(*para[0], **para[1])
            except TypeError:
                print 'parameter error'

class Remote(object):
    ''' wrapper for remote object '''
    def __init__(self, send):
        self.send = send
    def __getattr__(self, name):
        def method(*args, **kw):
            self.send( dump_call( name, args, kw ) )
        return method

def serve(obj, ip, port):
    ''' start a server '''
    return async_server.Listen( lambda : Dispatcher(obj), (ip, port), 6.0, 5 )

def connect(obj, ip, port):
    ''' connect a client '''
    return async_client.connect( Dispatcher(obj), (ip, port), 3)

