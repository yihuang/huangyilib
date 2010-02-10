class IoLoop(object):
    def __init__(self):
        self._handlers = {}

    def register(event_fd, event_type, callback):
        self._handlers[event_fd] = callback
        epoll.register(event_fd, event_type)

    def unregister(self, event_fd):
        delete self._handlers[event_fd]
        epoll.unregister(event_fd)

    def io_loop(self):
        event_pairs = epoll.poll()
        for event_fd, event_type in event_pairs:
            self._handlers[event_fd](event_type)


class Socket(object):
    def __init__(self, sock):
        self._sock = sock
        self._state = 

    def wait(self, event_type):
        '''
        wait for more data
        set readable callback or
        stackless channel.recv or
        '''
        self.update_io_state(event_type)
        '''
        #greenlet:
        self._greenlet = getcurrent()
        return main_thread.switch()
        '''
        '''
        # stackless
        if not hasattr(self, '_channels'):
            self._channels = defaultdict(stackless.channel)
        return self._channels[event_type].receive()
        '''
        '''
        # async
        # TODO
        '''

    def wakeup(self, event_type):
        '''
        wakeup handler
        callback or
        channel.send() or
        '''
        '''
        #greenlet
        self._greenlet.switch(event_type)
        '''
        '''
        # stackless
        self._channels[event_type].send()
        '''
        '''
        # async
        # TODO
        '''

    def recv(self, *args):
        while True:
            try:
                return self._sock.recv(*args)
            except error, ex:
                if ex[0]==EWOULDBLOCK: # need more data
                    pass
                else:
                    raise
            self.wait(READ)    

    def accept(self, *args):
        while True:
            try:
                client, addr = self._sock.accept()
                return Socket(_sock=client), addr
            except error, ex:
                if ex[0]==EWOULDBLOCK: # need more data
                    pass
                else:
                    raise
            self.wait(READ)

    def close(self):
        self.clear_io_state()
        self._sock.close()
        self._sock = None

    def update_io_state(self, state):
        io_loop.register(self._sock.fd, state, self.wakeup)
    def clear_io_state(self):
        io_loop.unregister(self._sock.fd)

class Stream(Socket):
    def __init__(self):
        self._buffer = ''

    def readbytes(self, bytes):
        _buffer = self._buffer
        while True:
            _buffer += self.recv(BUFFER_SIZE)
            if len(_buffer)>=bytes:
                result = _buffer[:bytes]
                self._buffer = _buffer[bytes:]
                return result

    def readline(self, delimiter='\n'):
        _buffer = self._buffer
        while True:
            _buffer += self.recv(BUFFER_SIZE)
            index = _buffer.rfind(delimiter)
            if index>=0:
                bytes = index+len(delimiter)
                result = _buffer[:bytes]
                self._buffer = _buffer[bytes:]
                return _buffer
