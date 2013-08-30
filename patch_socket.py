from socket import socket as _socket


class socket(object):
    'patch socket for testing'
    def __init__(self, *args, **kwargs):
        self._ss = _socket(*args, **kwargs)
        self.records = []
        self.recording = False
        self.replaying = False

    def start_record(self):
        self.recording = True
        self.replaying = False
        self.records = []

    def start_replay(self):
        self.recording = False
        self.replaying = True
        self.replay_records = self.records[:]

    def settimeout(self, n):
        return self._ss.settimeout(n)

    def connect(self, *args, **kwargs):
        return self._ss.connect(*args, **kwargs)

    def send(self, buf):
        if self.replaying:
            return len(buf)
        else:
            return self._ss.send(buf)

    def sendall(self, buf):
        if self.replaying:
            return len(buf)
        else:
            return self._ss.sendall(buf)

    def recv(self, size):
        if self.replaying:
            return self.replay_records.pop()
        buf = self._ss.recv(size)
        if self.recording:
            self.records.append(buf)
        return buf

    def close(self):
        return self._ss.close()

import socket as socketmodule
socketmodule.socket = socket

def run_with_recording(sock, func):
    sock.start_record()
    func()

def run_with_replay(sock, func):
    sock.start_replay()
    func()
