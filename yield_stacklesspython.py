#coding:utf-8
from collections import deque

'''
http://www.stackless.com/
'''

debuglevel = 0

readys = deque() # ready tasks [(tasklet, obj), ...]

class command(object):
    def __init__(self, func, *args, **kw):
        self.func = func
        self.args = args
        self.kw = kw

    def __call__(self, task):
        return self.func(task, *self.args, **self.kw)

class channel(object):
    ''' http://www.stackless.com/wiki/Channels '''
    def __init__(self):
        self.senders = deque() # sending tasks [(tasklet, obj), ...]
        self.receivers = deque() # receive tasks [tasklet, ...]

    def send(self, sender, obj):
        '''send data to the channel£¬if there is no receiver£¬then block
        the sender tasklet'''
        if debuglevel:
            print 'tasklet:',sender,'send data:',obj,';receivers:',len(self.receivers)
        if self.receivers:
            receiver = self.receivers.popleft()
            ready(sender, None)
            run(receiver, obj)
        else:
            self.senders.append( (sender, obj) )

    def receive(self, receiver):
        ''' receive data from channel£¬if there is no sender£¬then
        block the receiver tasklet'''
        if debuglevel:
            print 'tasklet:',receiver,'receive data ;senders:',len(self.senders)
        if self.senders:
            sender, obj = self.senders.popleft()
            ready(receiver,obj)
            run(sender, None)
        else:
            self.receivers.append(receiver)

class tasklet(object):
    '''http://www.stackless.com/wiki/Tasklets'''
    def __init__(self, func):
        self.func = func

    def __call__(self, *arg, **kw):
        '''add the genarator to the readys queue'''
        ready(self.func(*arg, **kw), None)

def run(task, obj):
    ''' run the task '''
    try:
        result = task.send(obj)
    except StopIteration:
        pass
    else:
        if isinstance(result, command):
            # execute the "system call request" 
            # tasklet can use: `yield command(func, ... )` to execute
            # some command in main tasklet.
            result(task)
        else:
            ready(task, None) # append to readys queue£¬wait to be executed

def ready(task, obj):
    ''' append to readys, wait to be executed '''
    readys.append( (task, obj) )

def schedule():
    ''' schedule the tasklets in readys '''
    while readys:
        task, obj = readys.popleft()
        run(task, obj)

# ============ test ===========

def simple_task(a):
    while True:
        print a
        yield None

def receiver(id, c):
    value = yield command(c.receive)
    print id,'receive', value
    while value:
        value = yield command(c.receive)
        print id,'received', value

def sender(id, c):
    value = 20
    while value:
        print id,'send',value
        yield command(c.send, value)
        value -= 1

def test_simple():
    tasklet(simple_task)(0)
    tasklet(simple_task)(10)
    tasklet(simple_task)(100)

def test_channel():
    c = channel()
    tasklet(receiver)('receiver1', c)
    tasklet(receiver)('receiver2', c)
    tasklet(sender)('sender1', c)
    c1 = channel()
    tasklet(receiver)('receiver3', c1)
    tasklet(sender)('sender2', c1)

if __name__=='__main__':
    #test_simple()
    test_channel()
    schedule()
